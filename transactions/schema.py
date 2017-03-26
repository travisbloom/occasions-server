from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from common.gql.types import AbstractModelType
from common.relay import Node
from products.models import Product
from .models import Transaction


class TransactionNode(AbstractModelType, DjangoObjectType):

    class Meta:
        interfaces = (Node, )
        model = Transaction


class Query(AbstractType):
    transactions = DjangoFilterConnectionField(TransactionNode)
