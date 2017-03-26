import pendulum
from factory.django import DjangoModelFactory

from events.models import (
    Person,
    User,
    Relationship
)


class UserFactory(factory.Factory):

    class Meta:
        model = User

    username = 'UserEmail@email.com'
    person__email = 'UserEmail@email.com'
    stripe_user_id = 'STRIP_USER_ID'
    person__first_name = 'User First Name'
    person__last_name = 'User Last Name'
    person__birth_date = pendulum.Date(1991, 1, 1)
    datetime_created = pendulum(2017, 1, 1)
    datetime_updated = pendulum(2017, 1, 1)


class PersonFactory(factory.Factory):

    class Meta:
        model = Person

    first_name = factory.Sequence(lambda num: 'FirstName#{}'.format(num))
    last_name = factory.Sequence(lambda num: 'LastName#{}'.format(num))
    email = factory.LazyAttribute(
        lambda obj: "{}.{}@email.com".format(obj.first_name, obj.last_name))
    birth_date = factory.Sequence(lambda num: pendulum.Date(
        1971, 1, 1).add(years=num, months=num * 2, days=num * 3))


class RelationshipFactory(factory.Factory):

    class Meta:
        model = Relationship

    to_person = factory.SubFactory(PersonFactory)
    relationship_type = factory.Interator([relation_type[1]
                                           for relation_type in Relationship.RELATIONSHIP_TYPE])
