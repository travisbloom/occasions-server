from graphene import relay, String, Field, AbstractType, ID, InputObjectType, InputField
from rest_framework import serializers

from common.exceptions import FormValuesException
from common.gql import get_pk_from_global_id
from locations.models import Location, AssociatedLocation
from locations.serializers.location import LocationSerializer
from locations.types import AssociatedLocationNode
from people.serializers import PersonWithRelationToCurrentUserField


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
        # TODO validate address against Lob
        person_id = get_pk_from_global_id(input.get('person_id'))
        serializer = CreateAssociatedLocationSerializer(
            data={
                **input,
                'person_id': person_id
            },
            context={'user': context.user}
        )
        if not serializer.is_valid():
            raise FormValuesException(serializer.errors)

        location = Location(**input.get('location'))
        location.save()
        associated_location = AssociatedLocation(
            location=location, person_id=person_id)
        associated_location.save()

        return CreateAssociatedLocation(
            associated_location=associated_location)


class LocationsMutations(AbstractType):
    create_associated_location = CreateAssociatedLocation.Field()
