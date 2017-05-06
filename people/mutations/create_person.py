from django.db.transaction import atomic
from graphene import relay, List, String, Field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from locations.models import AssociatedLocation, Location
from locations.mutation_inputs.location import LocationInput
from locations.serializers.location import LocationSerializer
from people.models import Person
from people.types import PersonNode


class CreatePersonInputSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)

    class Meta:
        model = Person
        fields = (
            'locations',
            'first_name',
            'last_name',
            'email',
            'birth_date',
        )

    @atomic
    def create(self, validated_data):
        locations = validated_data.pop('locations')
        person = Person(**validated_data)
        person.save()
        if not locations:
            raise ValidationError('People must have at least one address.')
        for location in locations:
            location = Location(**location)
            location.save()
            associated_location = AssociatedLocation(
                location=location, person=person)
            associated_location.save()
        return person


class CreatePerson(relay.ClientIDMutation):
    class Input:
        locations = List(LocationInput)
        first_name = String(required=True)
        last_name = String(required=True)
        email = String(required=True)
        birth_date = String(required=True)

    person = Field(PersonNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        input['creating_user_id'] = context.user
        serializer = CreatePersonInputSerializer(data=input)
        serializer.is_valid(raise_exception=True)
        person = serializer.save()

        return CreatePerson(person=person)
