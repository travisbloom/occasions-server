import factory

from events.models import EventType
from products.models import (
    Product
)

def reset_product_factories():
    ProductFactory.reset_sequence()


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    name = factory.Sequence(lambda num: "Product #{}".format(num))
    id = factory.LazyAttribute(lambda obj: "{} Slug".format(obj.name))
    cost_usd = factory.Sequence(lambda num: 2)
    description = factory.LazyAttribute(lambda obj: "{}'s Description".format(obj.name))
    main_image_url = "http://placehold.it/350x150"

    @factory.post_generation
    def post(self, create, extracted, **kwargs):
        self.event_types.add(EventType.objects.first())
