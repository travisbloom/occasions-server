from graphene import relay, ObjectType, Mutation, String, Field
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from products.models import Product
from .models import Transaction


class TransactionNode(DjangoNode):
    class Meta:
        model = Transaction

class Query(ObjectType):
    transaction = relay.NodeField(TransactionNode)
    transactions = DjangoFilterConnectionField(TransactionNode)

    class Meta:
        abstract = True

class CreateTransaction(relay.ClientIDMutation):

    class Input:
        product_id = String()
        associated_event_id = String()
        shipping_address_id = String()
        user_id = String()
        product_notes = String()
        cost_usd = String()

    transaction = Field('TransactionNode')

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        # TODO should grab the current price of the product and set as cost_usd
        transaction = Transaction(
            user_id=input.get('user_id'),
            cost_usd=input.get('cost_usd'),
            product_notes=input.get('product_notes'),
            product_id=input.get('product_id'),
            associated_event_id=input.get('associated_event_id'),
            shipping_address_id=input.get('shipping_address_id'),
        )
        transaction.save()
        return CreateTransaction(transaction=transaction)

class Mutation(ObjectType):
    create_transaction = Field(CreateTransaction)
