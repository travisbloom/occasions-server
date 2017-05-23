from django.db.models import Q
from graphene import List, Field, ConnectionField
from graphene_django import DjangoObjectType

from common.gql import AbstractModelType
from common.relay import Node
from events.models import Event, EventDate
from products.models import Product
from products.types import ProductNode


class EventDateNode(AbstractModelType, DjangoObjectType):
    class Meta:
        model = EventDate
        interfaces = (Node,)
        only_fields = (
            'date_start',
        )


class EventNode(AbstractModelType, DjangoObjectType):
    related_products = ConnectionField(ProductNode)
    event_dates = List(EventDateNode)
    next_date = Field(EventDateNode)
    event_types = List('events.types.EventTypeNode')

    class Meta:
        model = Event
        interfaces = (Node,)
        only_fields = (
            'name',
            'slug',
            'event_types',
            'is_default_event',
            'is_reoccuring_yearly',
            'datetime_created'
        )

    def resolve_next_date(self, args, context, info):
        return context.next_event_date_by_event_loader.load(self.pk)

    def resolve_event_dates(self, args, context, info):
        return context.event_date_by_event_loader.load(self.pk)

    def resolve_event_types(self, args, context, info):
        return context.event_types_by_event_loader.load(self.pk)

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
