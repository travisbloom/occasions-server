from events.factories import reset_event_factories, \
    generate_events_initial_testing_data
from locations.factories import reset_location_factories, generate_initial_location_data
from people.factories import reset_people_factories, \
    generate_people_initial_testing_data
from products.factories import reset_product_factories, generate_products_initial_data
from transactions.factories import reset_transaction_factories, generate_transactions_initial_data


def build_user_mock_data(
        with_products=False,
        with_associated_events=False,
        with_transactions=False,
):
    reset_event_factories()
    reset_location_factories()
    reset_people_factories()
    reset_product_factories()
    reset_transaction_factories()

    main_user = generate_people_initial_testing_data(small_sample=True)
    generate_initial_location_data(small_sample=True)

    if with_associated_events or with_transactions:
        generate_events_initial_testing_data(small_sample=True)

    if with_products or with_transactions:
        generate_products_initial_data(small_sample=True)

    if with_transactions:
        generate_transactions_initial_data(small_sample=True)

    return main_user
