from django.db.transaction import atomic
from graphene import relay, List, String, Field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.gql.get_pk_from_global_id import convert_input_global_ids_to_pks
from locations.models import AssociatedLocation, Location
from locations.mutation_inputs.location import LocationInput
from locations.serializers.location import LocationSerializer
from people.models import Person, RelationshipType, Relationship
from people.types import PersonNode


class CreatePersonInputSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
    relationship_type = serializers.PrimaryKeyRelatedField(queryset=RelationshipType.objects.all())

    class Meta:
        model = Person
        fields = (
            'locations',
            'first_name',
            'last_name',
            'gender',
            'relationship_type',
            'email',
            'birth_date',
        )

    @atomic
    def create(self, validated_data):
        locations = validated_data.pop('locations')
        relationship_type = validated_data.pop('relationship_type')
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
        relationship = Relationship(
            relationship_type=relationship_type,
            from_person=self.context['user'].person,
            to_person=person
        )
        relationship.save()
        return person


class CreatePerson(relay.ClientIDMutation):
    class Input:
        locations = List(LocationInput)
        first_name = String(required=True)
        last_name = String(required=True)
        gender = String(required=True)
        relationship_type = String(required=True)
        email = String(required=True)
        birth_date = String(required=True)

    person = Field(PersonNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        serializer = CreatePersonInputSerializer(
            data=convert_input_global_ids_to_pks(input, ('relationship_type',)),
            context={'user': context.user}
        )
        serializer.is_valid(raise_exception=True)
        person = serializer.save()

        return CreatePerson(person=person)
