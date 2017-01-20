from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from .models import Event, AssociatedEvent


class AssociatedEventNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = AssociatedEvent
        filter_fields = ['creating_person', 'receiving_person', 'event__event_type']


class EventNode(DjangoObjectType):
    event_type = String()  # FIXME https://github.com/graphql-python/graphene/issues/205

    class Meta:
        model = Event
        interfaces = (relay.Node, )
        filter_fields = ['is_default_event', 'event_type']


class Query(AbstractType):
    associated_event = relay.Node.Field(AssociatedEventNode)
    associated_events = DjangoFilterConnectionField(AssociatedEventNode)

    event = relay.Node.Field(EventNode)
    events = DjangoFilterConnectionField(EventNode)


class CreateAssociatedEvent(relay.ClientIDMutation):

    class Input:
        event_id = String(required=False)
        creating_person_id = String(required=True)
        receiving_person_id = String(required=True)

    associated_event = Field(lambda: AssociatedEventNode)

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        associated_event = AssociatedEvent(
            creating_person_id=input.get('creating_person_id'),
            receiving_person_id=input.get('receiving_person_id'),
            event_id=input.get('event_id'),
        )
        associated_event.save()
        return CreateAssociatedEvent(associated_event=associated_event)


class Mutation(AbstractType):
    create_associated_event = Field(CreateAssociatedEvent)
