from django.db.models import Q
from graphene import AbstractType, ID, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from common.gql.types import AbstractModelType
from common.relay import Node
from products.models import Product
from products.types import ProductNode
from .filters import EventFilter, EventTypeFilter
from .models import Event, AssociatedEvent, EventType


class AssociatedEventNode(AbstractModelType, DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = AssociatedEvent
        filter_fields = ['creating_person', 'receiving_person']


class EventTypeNode(AbstractModelType, DjangoObjectType):

    class Meta:
        model = EventType
        interfaces = (Node, )


class EventNode(AbstractModelType, DjangoObjectType):
    related_products = DjangoFilterConnectionField(ProductNode)

    class Meta:
        model = Event
        interfaces = (Node, )

    def resolve_related_products(self, args, context, info):
        return (
            Product.objects
            .filter(
                Q(event_id=self.id) |
                Q(event_types__in=[event_type for event_type in self.event_types.all()])
            )
            .order_by('-event_id')
        )


class EventQueries(AbstractType):
    associated_events = DjangoFilterConnectionField(AssociatedEventNode)
    events = DjangoFilterConnectionField(
        EventNode,
        filterset_class=EventFilter,
        event_types_pk_in=List(ID)
    )
    event_types = DjangoFilterConnectionField(
        EventTypeNode, filterset_class=EventTypeFilter)
