from itertools import cycle

import factory

from events.models import EventType
from products.models import (
    Product,
    ProductToEventType)


def reset_product_factories():
    ProductFactory.reset_sequence()


def generate_products_initial_data(small_sample):
    event_types_chain = cycle(EventType.objects.all())
    for _ in range(2 if small_sample else 20):
        product = ProductFactory()
        ProductToEventType.objects.bulk_create([
            ProductToEventType(event_type=next(event_types_chain), product=product),
            ProductToEventType(event_type=next(event_types_chain), product=product),
        ])


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda num: "Product #{}".format(num))
    id = factory.LazyAttribute(lambda obj: "{} Slug".format(obj.name))
    cost_usd = factory.Sequence(lambda num: 2)
    description = factory.LazyAttribute(lambda obj: "{}'s Description".format(obj.name))
    main_image_url = "http://placehold.it/350x150"
