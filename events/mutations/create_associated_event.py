from django.db import transaction
from graphene import relay, String, Field, ID, List, InputField, InputObjectType
from graphene.types.datetime import DateTime, Time

from common.exceptions import MutationException
from common.gql import get_pk_from_global_id
from events.models import Event, AssociatedEvent
from events.serializers import EventSerializer, AssociatedEventSerializer
from events.types.associated_event import AssociatedEventNode


class CreateEventInput(InputObjectType):
    event_types = List(ID)
    name = String(required=False)
    date_start = DateTime(required=False)
    time_start = Time(required=False)


class CreateAssociatedEvent(relay.ClientIDMutation):
    class Input:
        event = InputField(CreateEventInput)
        event_id = ID(required=False)
        receiving_person_id = ID(required=True)

    associated_event = Field(AssociatedEventNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, input, context, info):
        receiving_person_id = get_pk_from_global_id(input.get('receiving_person_id'))
        if not input.get('event_id'):
            event = input.get('event')
            if not event:
                raise MutationException('No event was sent')
            # TODO figure out how to set graphene to be a date not datetime
            if event.get('date_start'):
                event['date_start'] = event['date_start'].date()

            event_serializer = EventSerializer(data=event, context={
                'user': context.user,
                'receiving_person_id': receiving_person_id
            })
            event_serializer.is_valid(raise_exception=True)
            event = Event(**event)
            event.save()

        event_id = get_pk_from_global_id(input.get('event_id'))
        associated_event_serializer = AssociatedEventSerializer(
            data={
                'event': event_id,
                'creating_person': context.user.person.id,
                'receiving_person': receiving_person_id
            },
            context={
                'user': context.user,
                'receiving_person_id': receiving_person_id
            }
        )
        associated_event_serializer.is_valid(raise_exception=True)
        associated_event = AssociatedEvent(
            creating_person=context.user.person,
            receiving_person_id=receiving_person_id,
            event_id=event_id
        )
        associated_event.save()

        return CreateAssociatedEvent(associated_event=associated_event)
