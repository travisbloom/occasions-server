from django.db.transaction import atomic
from rest_framework import serializers

from locations.models import AssociatedLocation, Location
from locations.serializers.location import LocationSerializer
from people.serializers import PersonWithRelationToCurrentUserField


class AssociatedLocationSerializer(serializers.ModelSerializer):
    person_id = PersonWithRelationToCurrentUserField()
    location = LocationSerializer()

    class Meta:
        model = AssociatedLocation
        fields = ('person_id', 'location')

    @atomic
    def create(self, validated_data):
        location = Location(**validated_data.get('location'))
        location.save()
        associated_location = AssociatedLocation(
            location=location, person=validated_data.get('person_id'))
        associated_location.save()
        return associated_location
