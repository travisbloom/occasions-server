from graphene import AbstractType, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from common.gql.types import AbstractModelType
from common.relay import Node
from .models import Product


class ProductNode(AbstractModelType, DjangoObjectType):
    slug = ID(source='pk')

    class Meta:
        interfaces = (Node, )
        model = Product


class ProductQueries(AbstractType):
    products = DjangoFilterConnectionField(ProductNode)
