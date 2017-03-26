from events.factories import AssociatedEventFactory
from locations.factories import AssociatedLocationFactory
from people.factories import UserFactory, RelationshipFactory
from products.factories import ProductFactory
from transactions.factories import TransactionFactory


def build_user_mock_data(
    with_products=False,
    with_relationships=False,
    with_associated_events=False,
    with_transactions=False,
):
    UserFactory.reset_sequence()
    AssociatedLocationFactory.reset_sequence()
    user = UserFactory()
    for _ in range(2):
        AssociatedLocationFactory(person=user.person)

    if with_relationships or with_associated_events or with_transactions:
        RelationshipFactory.reset_sequence()
        for _ in range(10):
            RelationshipFactory(from_person=user.person)

    if with_associated_events or with_transactions:
        AssociatedEventFactory.reset_sequence()
        for num in range(10):
            relationships = user.person.from_relationships.all()
            AssociatedEventFactory(
                creating_person=user.person,
                receiving_person=relationships[1 if num % 2 == 0 else 0].from_person
            )

    if with_products or with_transactions:
        ProductFactory.reset_sequence()
        products = [ProductFactory() for _ in range(10)]

    if with_transactions:
        TransactionFactory.reset_sequence()
        for num in range(10):
            created_events = user.person.created_events.all()[num]
            receiving_person = created_events.receiving_person
            TransactionFactory(
                user=user,
                associated_event=created_events,
                receiving_person=receiving_person,
                product=products[-1 * num],
                associated_location=receiving_person.associated_locations.first()
            )

    return user
