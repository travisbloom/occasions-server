import factory

from transactions.models import (
    Transaction
)


def reset_transaction_factories():
    TransactionFactory.reset_sequence()


class TransactionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Transaction

    id = factory.Sequence(lambda num: num + 1)
    cost_usd = factory.LazyAttribute(lambda obj: obj.product.cost_usd)
    associated_location = factory.LazyAttribute(
        lambda obj: obj.receiving_person.associated_locations.first())
    product_notes = factory.Sequence(lambda num: "Product notes: {}".format(num))
    stripe_transaction_id = factory.Sequence(lambda num: "STRIPEID00{}".format(num))
