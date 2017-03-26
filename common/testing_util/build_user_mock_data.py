from events.factories import AssociatedEventFactory
from locations.factories import AssociatedLocationFactory
from people.factories import UserFactory, RelationshipFactory
from products.factories import ProductFactory
from transactions.factories import TransactionFactory


def build_user_mock_data(
    self,
    with_products=False,
    with_relationships=False,
    with_associated_events=False,
    with_transactions=False,
):
    user = UserFactory()
    [AssociatedLocationFactory(person=user.person) for _ in range(2)]

    if with_relationships or with_associated_events or with_transactions:
        [RelationshipFactory(from_person=user.person) for _ in range(10)]

    if with_associated_events or with_transactions:
        [
            AssociatedEventFactory(
                creating_person=user.person,
                receiving_person=user.from_relationships[1 if num % 2 == 0 else 0]
            )
            for num in range(10)
        ]

    if with_products or with_transactions:
        products = [ProductFactory() for _ in range(20)]

    if with_transactions:
        [
            TransactionFactory(
                user=user,
                associated_event=user.created_events,
                receiving_person=user.created_events.receiving_person,
                product=products[num],
                associated_location=user.created_events.receiving_person.associated_locations.first()
            ),
            for num in range(10)
        ]
