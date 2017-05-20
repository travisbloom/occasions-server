from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

from common.models import BaseModel


class User(AbstractUser):
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

    def __str__(self):
        return "{}".format(self.username)

    @property
    def full_name(self):
        return self.person.full_name


class Person(BaseModel):
    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'

    GENDER_CHOICES = (
        (GENDER_MALE, GENDER_MALE),
        (GENDER_FEMALE, GENDER_FEMALE)
    )
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
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField()

    def __str__(self):
        return "{}".format(self.full_name)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class RelationshipType(BaseModel):
    name = models.CharField(max_length=255, primary_key=True)
    from_person_male_display_name = models.CharField(max_length=100)
    from_person_female_display_name = models.CharField(max_length=100, default='', blank=True)
    to_person_male_display_name = models.CharField(max_length=100, default='', blank=True)
    to_person_female_display_name = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Relationship(BaseModel):

    from_person = models.ForeignKey(Person, related_name='from_relationships')
    to_person = models.ForeignKey(Person, related_name='to_relationships')
    relationship_type = models.ForeignKey(RelationshipType)

    @staticmethod
    def from_person_name(from_person, relationship_type):
        if from_person.gender == Person.GENDER_FEMALE and relationship_type.from_person_female_display_name:
            return relationship_type.from_person_female_display_name
        return relationship_type.from_person_male_display_name

    @staticmethod
    def to_person_name(to_person, relationship_type):
        if to_person.gender == Person.GENDER_FEMALE:
            if relationship_type.to_person_female_display_name:
                return relationship_type.to_person_female_display_name
            if relationship_type.from_person_female_display_name:
                return relationship_type.from_person_female_display_name
            return relationship_type.from_person_male_display_name
        elif relationship_type.to_person_male_display_name:
            return relationship_type.to_person_male_display_name
        return relationship_type.from_person_male_display_name

    def __str__(self):
        return "relation {} from {} to {}".format(
            self.relationship_type.name,
            self.from_person,
            self.to_person
        )
