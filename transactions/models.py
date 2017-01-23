from django.db import models
from django.core.exceptions import ValidationError

from model_utils import Choices

# Create your models here.
from common.models import BaseModel
from products.models import Product
from events.models import AssociatedEvent
from people.models import User
from locations.models import PersonLocation


class Transaction(BaseModel):
    STATUS_CREATED = 'created'
    STATUS_PAID = 'paid'
    STATUS_PENDING = 'pending'
    STATUS_COMPLETE = 'complete'

    STATUS_CHOICES = Choices(
        STATUS_CREATED,
        STATUS_PAID,
        STATUS_PENDING,
        STATUS_COMPLETE,
    )
    # TODO add lob-specific meta data
    user = models.ForeignKey(User)
    cost_usd = models.DecimalField(max_digits=5, decimal_places=2)
    product = models.ForeignKey(Product)
    associated_event = models.ForeignKey(AssociatedEvent)
    shipping_address = models.ForeignKey(PersonLocation)
    # ex: custom message for recipient on postcard
    product_notes = models.TextField()

    class Meta:
        default_related_name = 'transactions'

    def clean(self, *args, **kwargs):
        if (self.shipping_address.person_id != self.associated_event.receiving_person_id and
                self.shipping_address.person_id != self.associated_event.creating_person_id):
            raise ValidationError({
                'shipping_address': (
                    'The shipping address must belong to'
                    ' the creating or recieving person.'
                )
            })

        if not hasattr(self, 'cost_usd'):
            self.cost_usd = self.product.cost_usd

        super(Transaction, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Transaction, self).save(*args, **kwargs)
