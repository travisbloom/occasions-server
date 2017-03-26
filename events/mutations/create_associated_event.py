from django.db.models import Q
from rest_framework import serializers
from django.db import transaction

from graphene import relay, ObjectType, Mutation, String, Field, AbstractType, ID, List, InputField, InputObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from graphene.types.datetime import DateTime, Time

from common.exceptions import FormValuesException, MutationException
from common.gql.types import AbstractModelType
from products.models import Product
from products.schema import ProductNode

from people.serializers import PersonWithRelationToCurrentUserField

from events.filters import EventFilter, EventTypeFilter
from events.models import Event, AssociatedEvent, EventType
from events.schema import AssociatedEventNode
from events.serializers import EventSerializer, AssociatedEventSerializer


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
        event_id = input.get('event_id')
        if not event_id:
            event = input.get('event')
            if not event:
                raise MutationException('No event was sent')
            # TODO figure out how to set graphene to be a date not datetime
            if event.get('date_start'):
                event['date_start'] = event['date_start'].date()

            event_serializer = EventSerializer(data=event, context={
                'user': context.user,
                'receiving_person_id': input.get('receiving_person_id')
            })
            if not event_serializer.is_valid():
                raise FormValuesException(event_serializer.errors)
            event = Event(**event)
            event.save()
            event_id = event.id

        associated_event_serializer = AssociatedEventSerializer(
            data={
                'event': event_id,
                'creating_person': context.user.person.id,
                'receiving_person': input.get('receiving_person_id')
            },
            context={
                'user': context.user,
                'receiving_person_id': input.get('receiving_person_id')
            }
        )
        if not associated_event_serializer.is_valid():
            raise FormValuesException(associated_event_serializer.errors)
        associated_event = AssociatedEvent(
            creating_person=context.user.person,
            receiving_person_id=input.get('receiving_person_id'),
            event_id=event_id
        )
        associated_event.save()

        return CreateAssociatedEvent(associated_event=associated_event)
