from graphene_django import DjangoObjectType

from common.gql import AbstractModelType
from common.relay import Node
from events.models import EventType


class EventTypeNode(AbstractModelType, DjangoObjectType):

    class Meta:
        model = EventType
        interfaces = (Node, )
        only_fields = ('name', 'display_name')