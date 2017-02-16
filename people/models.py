from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from common.models import BaseModel


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    username = models.EmailField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    stripe_user_id = models.CharField(max_length=255, blank=True, default='')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)


class Person(BaseModel):
    # users should also be people in case we want to implement some
    # kind of "friending" mechanic between different users
    # ex: I add Dan from my contacts and then later on he signs up for the application
    # TODO understand usecase for this type of functionality, might be
    # overengineering
    user = models.OneToOneField(User, blank=True, null=True)
    relationships = models.ManyToManyField(
        'self',
        through='Relationship',
        symmetrical=False,
        blank=True
    )
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.CharField(max_length=30, blank=False)
    birth_date = models.DateField(null=True, blank=True)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class Relationship(BaseModel):
    TYPE_FRIENDS = 'friends'
    TYPE_SIBLINGS = 'siblings'
    TYPE_PARENT_TO_CHILD = 'parent_to_child'

    RELATIONSHIP_TYPE = Choices(
        TYPE_FRIENDS,
        TYPE_SIBLINGS,
        TYPE_PARENT_TO_CHILD
    )

    from_person = models.ForeignKey(Person, related_name='from_relationships')
    to_person = models.ForeignKey(Person, related_name='to_relationships')
    relationship_type = models.CharField(
        max_length=20, choices=RELATIONSHIP_TYPE)
