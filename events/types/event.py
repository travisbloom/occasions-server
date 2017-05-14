from django.db.models import Q
from graphene import List, Field, ConnectionField
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from common.gql import AbstractModelType
from common.relay import Node
from events.models import Event, EventDate
from products.models import Product
from products.types import ProductNode


class EventDateNode(AbstractModelType, DjangoObjectType):
    class Meta:
        model = EventDate
        interfaces = (Node, )
        only_fields = (
            'date_start',
        )


class EventNode(AbstractModelType, DjangoObjectType):
    related_products = ConnectionField(ProductNode)
    event_dates = List(EventDateNode)
    next_date = Field(EventDateNode)

    class Meta:
        model = Event
        interfaces = (Node, )

    def resolve_event_dates(self, args, context, info):
        return self.event_dates.all()

    def resolve_related_products(self, args, context, info):
        return (
            Product.objects
            .filter(
                Q(event_id=self.id) |
                Q(event_types__in=[
                    event_type for event_type in self.event_types.all()
                ])
            )
            .order_by('-event_id')
            .distinct()
        )

