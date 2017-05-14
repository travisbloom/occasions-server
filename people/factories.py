import factory
import pendulum
from factory import post_generation

from locations.factories import AssociatedLocationFactory
from people.models import (
    Person,
    User,
    Relationship
)


def reset_people_factories():
    PersonFactory.reset_sequence()
    UserFactory.reset_sequence()
    RelationshipFactory.reset_sequence()


class PersonFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Person

    id = factory.Sequence(lambda num: num + 1)
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

    id = factory.Sequence(lambda num: num + 1)
    stripe_user_id = 'cus_A4XJVCVTSgVA7G'


class RelationshipFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Relationship

    id = factory.Sequence(lambda num: num + 1)
    to_person = factory.SubFactory(PersonFactory)
    relationship_type = factory.Iterator([relation_type[1]
                                          for relation_type in Relationship.RELATIONSHIP_TYPE])
