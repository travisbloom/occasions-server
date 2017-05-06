from graphene_django import DjangoObjectType

from common.gql import AbstractModelType
from common.relay import Node
from events.models import AssociatedEvent


class AssociatedEventNode(AbstractModelType, DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = AssociatedEvent
        filter_fields = ['creating_person', 'receiving_person']