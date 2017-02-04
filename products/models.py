from django.db import models

from model_utils import Choices

# Create your models here.
from common.models import BaseModel
from events.models import EventType, Event


class ProductManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
                .prefetch_related('event_types')
        )


# TODO consider adding django-polymorphic to represent different types of products
class Product(BaseModel):
    TYPE_CARD = 'card'

    PRODUCT_TYPE = Choices(
        TYPE_CARD,
    )
    id = models.SlugField(primary_key=True)
    name = models.CharField(max_length=255)
    event_types = models.ManyToManyField(EventType)
    event = models.ForeignKey(Event, related_name='products', blank=True, null=True)
    cost_usd = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    product_type = models.TextField(max_length=30, choices=PRODUCT_TYPE, default=TYPE_CARD)
    main_image_url = models.URLField()

    objects = ProductManager()
