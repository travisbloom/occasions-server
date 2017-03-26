from graphene import relay, ObjectType, Mutation, String, Field, AbstractType, Argument, ID
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from common.gql.types import AbstractModelType
from .models import Product


class ProductNode(AbstractModelType, DjangoObjectType):
    slug = ID(source='pk')

    class Meta:
        interfaces = (relay.Node, )
        model = Product


class Query(AbstractType):
    products = DjangoFilterConnectionField(ProductNode)
