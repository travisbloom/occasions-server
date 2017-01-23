from django.db import models

from model_utils import Choices

# Create your models here.
from common.models import BaseModel


# TODO consider adding django-polymorphic to represent different types of products
class Product(BaseModel):
    TYPE_CARD = 'card'

    PRODUCT_TYPE = Choices(
        TYPE_CARD,
    )
    id = models.SlugField(primary_key=True)
    name = models.CharField(max_length=255)
    cost_usd = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    product_type = models.TextField(max_length=30, choices=PRODUCT_TYPE, default=TYPE_CARD)
    main_image_url = models.URLField()
