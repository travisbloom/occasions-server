from graphene import AbstractType

from transactions.mutations.create_stripe_user import CreateStripeUser
from transactions.mutations.create_transaction import CreateTransaction


class TransactionMutations(AbstractType):
    create_transaction = CreateTransaction.Field()
    create_stripe_user = CreateStripeUser.Field()
