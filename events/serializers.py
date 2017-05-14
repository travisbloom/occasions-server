from rest_framework import serializers

from events.models import Event, AssociatedEvent
from people.serializers import PersonWithRelationToCurrentUserField


class EventDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'event',
            'start_date',
        )


class EventSerializer(serializers.ModelSerializer):
    event_type_ids = serializers.PrimaryKeyRelatedField(
        source='event_types', many=True, read_only=True)
    event_dates = EventDateSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            'name',
            'event_type_ids',
            'event_dates',
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
