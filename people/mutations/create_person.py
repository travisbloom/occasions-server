from django.db.transaction import atomic
from graphene import relay, List, String, Field
from rest_framework import serializers

from common.exceptions import FormValuesException
from locations.mutation_inputs.location import LocationInput
from locations.serializers.location import LocationSerializer
from people.models import Person
from people.types import PersonNode


class CreatePersonInputSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)

    class Meta:
        model = Person
        fields = (
            'first_name',
            'last_name',
            'email',
            'birth_date',
        )

    @atomic
    def create(self, validated_data):
        locations = validated_data.pop('profile')
        person = Person(**validated_data)
        person.save()
        for location in locations:
            location = LocationSerializer(**location)
            location.save()
        return user

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
        input['creating_user_id'] = context.user
        serializer = CreatePersonInputSerializer(data=input)
        serializer.is_valid(raise_exception=True)
        person = serializer.save()

        return CreatePersonMutation(person=person)
