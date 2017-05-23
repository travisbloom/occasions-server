from graphene_django import DjangoObjectType

from common.gql import AbstractModelType
from common.relay import Node
from events.models import AssociatedEvent


class AssociatedEventNode(AbstractModelType, DjangoObjectType):
    class Meta:
        interfaces = (Node,)
        model = AssociatedEvent
        filter_fields = ('creating_person', 'receiving_person')
        only_fields = (
            'creating_person',
            'receiving_person',
            'event',
            'transactions'
        )

    def resolve_creating_person(self, args, context, info):
        return context.person_loader.load(self.creating_person_id)

    def resolve_receiving_person(self, args, context, info):
        return context.person_loader.load(self.receiving_person_id)

    def resolve_event(self, args, context, info):
        return context.event_loader.load(self.event_id)
