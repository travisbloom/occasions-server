from events.factories import AssociatedEventFactory, EventFactory, reset_event_factories
from locations.factories import AssociatedLocationFactory, reset_location_factories
from people.factories import UserFactory, RelationshipFactory, PersonFactory, reset_people_factories
from products.factories import ProductFactory, reset_product_factories
from transactions.factories import TransactionFactory, reset_transaction_factories


def build_user_mock_data(
    with_products=False,
    with_relationships=False,
    with_associated_events=False,
    with_transactions=False,
):
    reset_event_factories()
    reset_location_factories()
    reset_people_factories()
    reset_product_factories()
    reset_transaction_factories()

    user_email = "useremail@email.com"
    user = UserFactory(username=user_email)
    user_person = PersonFactory(
        id=1000,
        user=user,
        email=user_email,
        first_name='UserFirstName',
        last_name='UserLastName'
    )
    PersonFactory.reset_sequence()
    for _ in range(2):
        AssociatedLocationFactory(person=user.person)

    if with_relationships or with_associated_events or with_transactions:
        for _ in range(10):
            RelationshipFactory(from_person=user.person)

    if with_associated_events or with_transactions:
        for num in range(10):
            relationships = user.person.from_relationships.all()
            AssociatedEventFactory(
                creating_person=user.person,
                receiving_person=relationships[num].to_person
            )

    if with_products or with_transactions:
        products = [ProductFactory() for _ in range(10)]

    if with_transactions:
        for num in range(10):
            created_events = user.person.created_events.all()[num]
            receiving_person = created_events.receiving_person
            TransactionFactory(
                user=user,
                associated_event=created_events,
                receiving_person=receiving_person,
                product=products[num],
                associated_location=receiving_person.associated_locations.first()
            )

    return user
