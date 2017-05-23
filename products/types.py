from graphene import AbstractType, ID, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from common.gql.types import AbstractModelType
from common.relay import Node
from .models import Product


class ProductNode(AbstractModelType, DjangoObjectType):
    slug = ID(source='pk')
    event_types = List('events.types.EventTypeNode')

    class Meta:
        interfaces = (Node,)
        model = Product
        only_fields = (
            'name',
            'event',
            'cost_usd',
            'description',
            'product_type',
            'main_image_url',
        )

    def resolve_event_types(self, args, context, info):
        return context.event_types_by_product_loader.load(self.pk)

    def resolve_event(self, args, context, info):
        if self.event_id:
            return context.event_loader.load(self.event_id)


class ProductQueries(AbstractType):
    products = DjangoFilterConnectionField(ProductNode)
