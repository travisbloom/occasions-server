import os
from itertools import chain, cycle

import factory
import pendulum
from django.contrib.auth.hashers import make_password
from factory import post_generation

from locations.factories import AssociatedLocationFactory
from people.default_data.relationship_types import generate_default_relationship_types
from people.models import (
    Person,
    User,
    Relationship,
    RelationshipType)


def reset_people_factories():
    PersonFactory.reset_sequence()
    UserFactory.reset_sequence()
    RelationshipFactory.reset_sequence()


def generate_people_initial_testing_data(small_sample):
    relationship_types = generate_default_relationship_types()
    main_user = User(
        username='travisbloom@gmail.com',
        stripe_user_id=os.environ.get('OCCASIONS_STRIPE_TEST_USER_ID'),
        is_staff=True,
        is_superuser=True
    )
    main_user.set_password('changeme')
    main_user.save()
    main_person = Person(
        user=main_user,
        first_name='Travis',
        last_name='Bloom',
        email='travisbloom@gmail.com',
        birth_date=pendulum.create(1991, 2, 23).date()
    )
    main_person.save()
    users = []
    if not small_sample:
        users = [
            UserFactory(person=None)
            for _ in range(3)
        ]
        for user in users:
            PersonFactory(user=user)
    people = [
        PersonFactory()
        for _ in range(2 if small_sample else 20)
    ]
    people_chain = cycle(people)
    relationship_types_chain = cycle(relationship_types)
    for user in [main_user] + users:
        for _ in range(2 if small_sample else 9):
            relationship = Relationship(
                relationship_type=next(relationship_types_chain),
                from_person=user.person,
                to_person=next(people_chain)
            )
            relationship.save()
    return main_user


class PersonFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Person

    first_name = factory.Sequence(lambda num: 'FirstName#{}'.format(num))
    last_name = factory.Sequence(lambda num: 'LastName#{}'.format(num))
    email = factory.LazyAttribute(
        lambda obj: User.objects.normalize_email(
            "{}.{}@email.com".format(obj.first_name, obj.last_name)
        )
    )
    birth_date = factory.Sequence(lambda num: pendulum.now().add(years=num, months=num * 2, days=num * 3))
    location = factory.RelatedFactory(AssociatedLocationFactory, 'person')


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    stripe_user_id = 'cus_A4XJVCVTSgVA7G'
    person = factory.SubFactory(PersonFactory)
    username = factory.Sequence(
        lambda num: User.objects.normalize_email(
            "email_{}@email.com".format(num)
        )
    )
    password = factory.Sequence(
        lambda num: make_password("password{}".format(num))
    )


class RelationshipFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Relationship

    to_person = factory.SubFactory(PersonFactory)
    relationship_type = factory.Iterator(lambda: RelationshipType.objects.all())
