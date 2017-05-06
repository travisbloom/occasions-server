from graphene import relay, List, String, Field
from rest_framework import serializers

from common.exceptions import FormValuesException
from locations.mutation_inputs.location import LocationInput
from locations.serializers.location import LocationSerializer
from people.models import Person
from people.types import PersonNode


class CreatePersonInputSerializer(serializers.ModelSerializer):
    locations = serializers.ListSerializer(LocationSerializer)

    class Meta:
        model = Person
        fields = (
            'first_name',
            'last_name',
            'email',
            'birth_date',
        )

    def validate_locations(self, obj):
        return obj


class CreatePersonMutation(relay.ClientIDMutation):
    class Input:
        locations = List(LocationInput)
        first_name = String(required=True)
        last_name = String(required=True)
        email = String(required=True)
        birth_date = String(required=True)

    person = Field(PersonNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        serializer = CreatePersonInputSerializer(data=input)
        serializer.is_valid()
        if not serializer.is_valid():
            raise FormValuesException(serializer.errors)

        person = serializer.save()

        return CreatePersonMutation(person=person)
