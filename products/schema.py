from graphene import relay, ObjectType, Mutation, String, Field
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from .models import Product


class ProductNode(DjangoNode):
    class Meta:
        model = Product

class Query(ObjectType):
    product = relay.NodeField(ProductNode)
    products = DjangoFilterConnectionField(ProductNode)

    class Meta:
        abstract = True
