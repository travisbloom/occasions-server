from graphene import AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from common.gql.types import AbstractModelType
from common.relay import Node
from .models import Transaction


class TransactionNode(AbstractModelType, DjangoObjectType):
    class Meta:
        interfaces = (Node,)
        model = Transaction
        only_fields = (
            'user',
            'receiving_person',
            'cost_usd',
            'product',
            'associated_event',
            'associated_event_date',
            'associated_location',
            'product_notes',
            'stripe_transaction_id',
            'datetime_created',
            'datetime_updated'
        )

    def resolve_receiving_person(self, args, context, info):
        return context.person_loader.load(self.receiving_person_id)

    def resolve_associated_event(self, args, context, info):
        return context.associated_event_loader.load(self.associated_event_id)

    def resolve_associated_event_date(self, args, context, info):
        return context.event_date_loader.load(self.associated_event_date_id)

    def resolve_associated_location(self, args, context, info):
        return context.associated_location_loader.load(self.associated_location_id)

    def resolve_product(self, args, context, info):
        return context.product_loader.load(self.product_id)


class TransactionStaffQueries(AbstractType):
    transactions = DjangoFilterConnectionField(TransactionNode)
