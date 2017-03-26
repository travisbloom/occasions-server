from django.conf import settings
import stripe
import logging

logger = logging.getLogger('occasions')
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_user(payload, user, request):
    try:
        customer = stripe.Customer.create(
            source=payload['strip_transaction_id'],
            email=payload.get('email'),
            metadata={
                'user_id': user.id,
            }
        )
    except Exception as e:
        logger.exception(
            'create_stripe_user request failed', extra={
                'request': request})
        raise(e)

    user.stripe_user_id = customer.id
    user.save()


def mock_create_stripe_charge(user, transaction, request):
    transaction.stripe_transaction_id = 'TESTING_CHARGE_ID'
    transaction.status = transaction.STATUS_PAID
    transaction.save()


def create_stripe_charge(user, transaction, request):
    location = transaction.associated_location.location
    try:
        charge = stripe.Charge.create(
            amount=int(transaction.cost_usd * 100),  # stripe works in cents
            currency='usd',
            description="{product} ({event}) for {receiving_person}".format(
                product=transaction.product.name,
                event=transaction.associated_event.event.name,
                receiving_person=transaction.receiving_person.full_name
            ),
            receipt_email=user.username,
            customer=user.stripe_user_id,
            statement_descriptor='Occasions App',
            metadata={
                'user_id': user.id,
                'transaction_id': transaction.id,
                'product_id': transaction.product.id,
                'associated_event_id': transaction.associated_event.id,
                'event_id': transaction.associated_event.event.id,
                'location_id': location.id
            },
            shipping={
                'name': location.display_name,
                'address': {
                    'line1': location.street_address_line1,
                    'line2': location.street_address_line2,
                    'postal_code': location.postal_code,
                    'city': location.city,
                    'state': location.state,
                    'country': location.country,
                }
            }
        )
    except Exception as e:
        logger.exception(
            'create_strip_charge request failed', extra={
                'request': request})
        raise (e)

    transaction.stripe_transaction_id = charge.id
    transaction.status = transaction.STATUS_PAID
    transaction.save()
