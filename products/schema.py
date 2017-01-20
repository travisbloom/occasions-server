from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from .models import Product


class ProductNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = Product


class Query(AbstractType):
    product = relay.Node.Field(ProductNode)
    products = DjangoFilterConnectionField(ProductNode)
