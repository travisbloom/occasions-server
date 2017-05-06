from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from common.gql import AbstractModelType
from common.relay import Node
from events.models import Event
from products.models import Product
from products.types import ProductNode


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