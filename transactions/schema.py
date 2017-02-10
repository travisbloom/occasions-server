from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from common.gql.types import AbstractModelType
from products.models import Product
from .models import Transaction


class TransactionNode(AbstractModelType, DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = Transaction


class Query(AbstractType):
    transaction = relay.Node.Field(TransactionNode)
    transactions = DjangoFilterConnectionField(TransactionNode)
