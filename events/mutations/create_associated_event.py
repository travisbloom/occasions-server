from django.db import transaction
from graphene import relay, String, Field, ID, List, InputField, InputObjectType

from common.gql.get_pk_from_global_id import convert_input_global_ids_to_pks
from events.serializers import AssociatedEventSerializer
from events.types.associated_event import AssociatedEventNode


class CreateEventNextDateInput(InputObjectType):
    date_start = String()


class CreateEventInput(InputObjectType):
    event_types = List(ID)
    name = String(required=False)
    next_date = InputField(CreateEventNextDateInput)


class CreateAssociatedEvent(relay.ClientIDMutation):
    class Input:
        event = InputField(CreateEventInput)
        event_id = ID(required=False)
        receiving_person_id = ID(required=True)

    associated_event = Field(AssociatedEventNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, input, context, info):
        formatted_input = convert_input_global_ids_to_pks(input, ('event_types',))
        associated_event_serializer = AssociatedEventSerializer(
            data=formatted_input,
            context={
                'user': context.user,
            }
        )
        associated_event_serializer.is_valid(raise_exception=True)
        associated_event = associated_event_serializer.save()
        return CreateAssociatedEvent(associated_event=associated_event)
