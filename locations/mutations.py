from graphene import relay, ObjectType, Mutation, String, Field, AbstractType, ID, InputObjectType, InputField
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from rest_framework import serializers

from people.models import Person
from people.serializers import PersonWithRelationToCurrentUserField
from .models import Location, AssociatedLocation
from .schema import AssociatedLocationNode


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


class CreateAssociatedLocationSerializer(serializers.Serializer):
    person_id = PersonWithRelationToCurrentUserField()
    location = LocationSerializer()


class CreateLocationInput(InputObjectType):
    street_address_line1 = String(required=True)
    street_address_line2 = String(required=False)
    postal_code = String(required=True)
    city = String(required=True)
    state = String(required=True)


class CreateAssociatedLocation(relay.ClientIDMutation):

    class Input:
        person_id = ID(required=True)
        location = InputField(CreateLocationInput)

    associated_location = Field(AssociatedLocationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        serializer = CreateAssociatedLocationSerializer(data=input, context={'user': context.user})
        if not serializer.is_valid():
            raise Exception(serializer.errors)

        location = Location(**input.get('location'))
        location.save()
        associated_location = AssociatedLocation(location=location, person_id=input.get('person_id'))
        associated_location.save()

        return CreateAssociatedLocation(associated_location=associated_location)


class LocationsMutation(AbstractType):
    create_associated_location = CreateAssociatedLocation.Field()
