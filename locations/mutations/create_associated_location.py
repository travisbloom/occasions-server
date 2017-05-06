from graphene import relay, Field, AbstractType, ID, InputField

from common.gql.get_pk_from_global_id import convert_input_global_ids_to_pks
from locations.mutation_inputs.location import LocationInput
from locations.serializers.associated_location import AssociatedLocationSerializer
from locations.types import AssociatedLocationNode


class CreateAssociatedLocation(relay.ClientIDMutation):

    class Input:
        person_id = ID(required=True)
        location = InputField(LocationInput)

    associated_location = Field(AssociatedLocationNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        # TODO validate address against Lob
        converted_input = convert_input_global_ids_to_pks(input)
        serializer = AssociatedLocationSerializer(
            data=converted_input,
            context={'user': context.user}
        )
        serializer.is_valid(raise_exception=True)
        associated_location = serializer.save()
        return CreateAssociatedLocation(
            associated_location=associated_location)


class LocationsMutations(AbstractType):
    create_associated_location = CreateAssociatedLocation.Field()
