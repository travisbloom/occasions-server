import pendulum
import factory

from products.models import (
    Product
)


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    name = factory.Sequence(lambda num: "Product #{}".format(num))
    id = factory.LazyAttribute(lambda obj: "{} Slug".format(obj.name))
    cost_usd = factory.Sequence(lambda num: 2)
    description = factory.LazyAttribute(lambda obj: "{}'s Description".format(obj.name))
    main_image_url = "http://placehold.it/350x150"

    # @factory.post_generation
    # def event_types(self, create, extracted, **kwargs):
    #     if extracted:
    #         # A list of groups were passed in, use them
    #         for event_type in extracted:
    #             self.event_types.add(event_type)
    #     else:
    #         self.event_types.add(EventType.objects.first())
