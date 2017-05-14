from django.core.exceptions import ValidationError
from django.db import models
from model_utils import Choices

# Create your models here.
from common.models import BaseModel
from events.models import AssociatedEvent
from locations.models import AssociatedLocation
from people.models import User, Person
from products.models import Product


class TransactionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'product',
            'associated_event',
            'associated_event__event',
            'associated_location',
            'associated_location__location'
        )


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
    receiving_person = models.ForeignKey(Person)
    cost_usd = models.DecimalField(max_digits=5, decimal_places=2)
    product = models.ForeignKey(Product)
    associated_event = models.ForeignKey(
        AssociatedEvent, blank=True, null=True)
    associated_location = models.ForeignKey(AssociatedLocation)
    # ex: custom message for recipient on postcard
    product_notes = models.TextField()
    stripe_transaction_id = models.CharField(
        max_length=255, blank=True, default='')

    objects = TransactionManager()

    class Meta:
        default_related_name = 'transactions'

    def __str__(self):
        return "{} from {} to {} on {}".format(
            self.product,
            self.user.person,
            self.receiving_person,
            self.datetime_created
        )

    def clean(self, *args, **kwargs):
        if (self.associated_location.person_id != self.associated_event.receiving_person_id and
                self.associated_location.person_id != self.associated_event.creating_person_id):
            raise ValidationError({
                'associated_location': (
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
