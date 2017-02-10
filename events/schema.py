from django.db.models import Q

from graphene import relay, ObjectType, Mutation, String, Field, AbstractType, ID
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from common.gql.types import AbstractModelType
from .models import Event, AssociatedEvent, EventType
from products.models import Product
from products.schema import ProductNode

class AssociatedEventNode(AbstractModelType, DjangoObjectType):

    class Meta:
        interfaces = (relay.Node, )
        model = AssociatedEvent
        filter_fields = ['creating_person', 'receiving_person']


class EventTypeNode(AbstractModelType, DjangoObjectType):

    class Meta:
        model = EventType
        interfaces = (relay.Node, )


class EventNode(AbstractModelType, DjangoObjectType):
    related_products = DjangoFilterConnectionField(ProductNode)

    class Meta:
        model = Event
        interfaces = (relay.Node, )

    def resolve_related_products(self, args, context, info):
        return (
            Product.objects
                .filter(
                    Q(event_id=self.id) |
                    Q(event_types__in=[event_type.id for event_type in self.event_types.all()])
                )
                .order_by('-event_id')
        )



class Query(AbstractType):
    associated_event = relay.Node.Field(AssociatedEventNode)
    associated_events = DjangoFilterConnectionField(AssociatedEventNode)

    event = relay.Node.Field(EventNode)
    events = DjangoFilterConnectionField(EventNode)

    event_type = relay.Node.Field(EventTypeNode)
    event_types = DjangoFilterConnectionField(EventTypeNode)


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
