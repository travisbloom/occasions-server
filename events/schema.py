from django.db.models import Q

from graphene import relay, ObjectType, Mutation, String, Field, AbstractType, ID, List
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from common.gql.types import AbstractModelType
from .models import Event, AssociatedEvent, EventType
from products.models import Product
from products.schema import ProductNode
from .filters import EventFilter, EventTypeFilter


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
                Q(event_types__in=[event_type for event_type in self.event_types.all()])
            )
            .order_by('-event_id')
        )


class Query(AbstractType):
    associated_event = relay.Node.Field(AssociatedEventNode)
    associated_events = DjangoFilterConnectionField(AssociatedEventNode)

    event = relay.Node.Field(EventNode)
    events = DjangoFilterConnectionField(
        EventNode,
        filterset_class=EventFilter,
        event_types_pk_in=List(ID)
    )

    event_type = relay.Node.Field(EventTypeNode)
    event_types = DjangoFilterConnectionField(
        EventTypeNode, filterset_class=EventTypeFilter)

    def resolve_events(self, variables, context, info, *foo, **kwargs):
        qs = Event.objects
        if variables.get('event_types_pk_in'):
            qs = qs.filter(event_types__pk__in=variables.get(
                'event_types_pk_in')).distinct()
        qs = EventFilter(data=variables, queryset=qs).qs
        return qs
