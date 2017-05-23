from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.models import Event, AssociatedEvent, EventDate, EventType, EventToEventType
from people.serializers import PersonWithRelationToCurrentUserField


class EventDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        fields = (
            'date_start',
        )


class EventSerializer(serializers.ModelSerializer):
    event_types = serializers.PrimaryKeyRelatedField(queryset=EventType.objects.all(), many=True)
    next_date = EventDateSerializer()

    class Meta:
        model = Event
        fields = (
            'name',
            'event_types',
            'next_date'
        )

    def create(self, validated_data):
        next_date = validated_data.pop('next_date')
        event_types = validated_data.pop('event_types')
        event = Event(**validated_data)
        event.save()
        EventToEventType.objects.bulk_create([
            EventToEventType(event_type=event_type, event=event)
            for event_type in event_types
        ])
        event_date = EventDate(**next_date, event=event)
        event_date.save()
        return event


class AssociatedEventSerializer(serializers.ModelSerializer):
    receiving_person_id = PersonWithRelationToCurrentUserField()
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.filter(is_default_event=True), required=False)
    event = EventSerializer(required=False)

    class Meta:
        model = AssociatedEvent
        fields = (
            'event',
            'event_id',
            'receiving_person_id',
        )

    def create(self, validated_data):
        new_event = validated_data.pop('event', None)
        existing_event = validated_data.pop('event_id', None)
        if not existing_event:
            if not new_event:
                raise ValidationError({
                    'event': 'You must have a new event or event_id attached to this associated event.'
                })
            else:
                existing_event = EventSerializer().create(new_event)
        associated_event = AssociatedEvent(
            event=existing_event,
            receiving_person=validated_data.get('receiving_person_id'),
            creating_person=self.context['user'].person
        )
        associated_event.save()
        return associated_event
