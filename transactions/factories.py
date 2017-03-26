import pendulum
from factory.django import DjangoModelFactory

from transactions.models import (
    Transaction
)


class TransactionFactory(factory.Factory):

    class Meta:
        model = Transaction

    cost_usd = factory.LazyAttribute(obj.product.cost_usd)
    associated_location = factory.LazyAttribute(obj.receiving_person.associated_locations.first())
    product_notes = factory.Sequence(lambda num: "Product notes: {}".format(num))
    stripe_transaction_id = factory.Sequence(lambda num: "STRIPEID00{}".format(num))
