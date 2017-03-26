from rest_framework import serializers

from people.serializers import PersonWithRelationToCurrentUserField

from events.models import Event, AssociatedEvent, EventType


class EventSerializer(serializers.ModelSerializer):
    event_type_ids = serializers.PrimaryKeyRelatedField(
        source='event_types', many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'name',
            'event_type_ids',
            'date_start',
            'time_start',
        )


class AssociatedEventSerializer(serializers.ModelSerializer):
    receiving_person = PersonWithRelationToCurrentUserField()

    class Meta:
        model = AssociatedEvent
        fields = (
            'event',
            'receiving_person',
            'creating_person',
        )
