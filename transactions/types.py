from graphene import AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from common.gql.types import AbstractModelType
from common.relay import Node
from .models import Transaction


class TransactionNode(AbstractModelType, DjangoObjectType):

    class Meta:
        interfaces = (Node, )
        model = Transaction


class TransactionQueries(AbstractType):
    transactions = DjangoFilterConnectionField(TransactionNode)
