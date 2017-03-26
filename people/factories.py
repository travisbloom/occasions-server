import pendulum
import factory

from people.models import (
    Person,
    User,
    Relationship
)


class PersonFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Person

    first_name = factory.Sequence(lambda num: 'FirstName#{}'.format(num))
    last_name = factory.Sequence(lambda num: 'LastName#{}'.format(num))
    email = factory.LazyAttribute(
        lambda obj: "{}.{}@email.com".format(obj.first_name, obj.last_name))
    birth_date = factory.Sequence(lambda num: pendulum.Date(
        1971, 1, 1).add(years=num, months=num * 2, days=num * 3))


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = 'UserEmail@email.com'
    stripe_user_id = 'STRIP_USER_ID'
    person = factory.SubFactory(PersonFactory)
    datetime_created = pendulum.create(2017, 1, 1)
    datetime_updated = pendulum.create(2017, 1, 1)


class RelationshipFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Relationship

    to_person = factory.SubFactory(PersonFactory)
    relationship_type = factory.Iterator([relation_type[1]
                                          for relation_type in Relationship.RELATIONSHIP_TYPE])
