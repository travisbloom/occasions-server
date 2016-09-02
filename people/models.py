from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from occasions.models import BaseModel

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
    #we want to make first_name and last_name required fields
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)


class Person(BaseModel):
    user = models.OneToOneField(User, blank=True, null=True)
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, blank=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.CharField(max_length=30, blank=False)
    birth_date = models.DateField(null=True, blank=True)


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
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPE)
