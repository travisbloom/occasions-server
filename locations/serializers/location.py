from rest_framework import serializers

from locations.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'street_address_line1',
            'street_address_line2',
            'postal_code',
            'city',
            'state',
        )
