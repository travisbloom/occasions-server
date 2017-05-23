from itertools import cycle

import factory

from people.models import User
from products.models import Product
from transactions.models import (
    Transaction
)


def reset_transaction_factories():
    TransactionFactory.reset_sequence()


def generate_transactions_initial_data(small_sample):
    products_chain = cycle(Product.objects.all())
    users = User.objects.all().prefetch_related(
        'person',
        'person__created_events',
        'person__created_events__receiving_person',
        'person__created_events__receiving_person__associated_locations',
        'person__created_events__event',
        'person__created_events__event__event_dates',
    )

    for user in users:
        for associated_event in user.person.created_events.all():
            for _ in range(2 if small_sample else 8):
                TransactionFactory(
                    user=user,
                    receiving_person=associated_event.receiving_person,
                    product=next(products_chain),
                    associated_event=associated_event,
                    associated_event_date=associated_event.event.event_dates.first(),
                    associated_location=associated_event.receiving_person.associated_locations.first()
                )


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    id = factory.Sequence(lambda num: num + 1)
    cost_usd = factory.LazyAttribute(lambda obj: obj.product.cost_usd)
    associated_location = factory.LazyAttribute(
        lambda obj: obj.receiving_person.associated_locations.first())
    product_notes = factory.Sequence(lambda num: "Product notes: {}".format(num))
    stripe_transaction_id = factory.Sequence(lambda num: "STRIPEID00{}".format(num))
