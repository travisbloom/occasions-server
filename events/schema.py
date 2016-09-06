from graphene import relay, ObjectType, Mutation, String, Field
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from .models import Event, AssociatedEvent


class AssociatedEventNode(DjangoNode):
    class Meta:
        model = AssociatedEvent

class EventNode(DjangoNode):
    class Meta:
        model = Event

class Query(ObjectType):
    associated_event = relay.NodeField(AssociatedEventNode)
    associated_events = DjangoFilterConnectionField(AssociatedEventNode)

    event = relay.NodeField(EventNode)
    events = DjangoFilterConnectionField(EventNode)

    class Meta:
        abstract = True

class CreateAssociatedEvent(relay.ClientIDMutation):

    class Input:
        event_id = String(required=False)
        creating_person_id = String(required=True)
        receiving_person_id = String(required=True)

    associated_event = Field('AssociatedEventNode')

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        associated_event = AssociatedEvent(
            creating_person_id=input.get('creating_person_id'),
            receiving_person_id=input.get('receiving_person_id'),
            event_id=input.get('event_id'),
        )
        associated_event.save()
        return CreateAssociatedEvent(associated_event=associated_event)

class EventMutation(ObjectType):
    create_associated_event = Field(CreateAssociatedEvent)
