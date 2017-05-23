import logging

from django.conf import settings
from graphene import relay, String, Field, ID
from rest_framework import serializers

from common.exceptions import MutationException
from common.gql.get_pk_from_global_id import convert_input_global_ids_to_pks
from events.models import AssociatedEvent
from locations.models import AssociatedLocation
from people.serializers import PersonWithRelationToCurrentUserField
from products.models import Product
from transactions.models import Transaction
from transactions.stripe import create_stripe_charge, mock_create_stripe_charge
from transactions.types import TransactionNode

logger = logging.getLogger('occasions')


class LocationRelatedToPersonField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return AssociatedLocation.objects.filter(
            person_id=self.context['receiving_person_id'])


class AssociatedEventRelatedToPersonField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return AssociatedEvent.objects.filter(
            receiving_person_id=self.context['receiving_person_id'],
            creating_person=self.context['user'].person
        )


class CreateTransactionSerializer(serializers.Serializer):
    receiving_person_id = PersonWithRelationToCurrentUserField()
    associated_location_id = LocationRelatedToPersonField()
    associated_event_id = AssociatedEventRelatedToPersonField()
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())
    product_notes = serializers.CharField()


class CreateTransaction(relay.ClientIDMutation):
    class Input:
        product_id = ID(required=False)
        associated_event_id = ID(required=False)
        associated_location_id = ID(required=False)
        receiving_person_id = ID(required=False)
        product_notes = String(required=False)

    transaction = Field(TransactionNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if not context.user.stripe_user_id:
            error_msg = 'User tried to create a transaction before they have a stripe account'
            logger.warning(error_msg, extra={'request': context})
            raise MutationException(error_msg)
        formatted_input = convert_input_global_ids_to_pks(input)
        serializer = CreateTransactionSerializer(data=formatted_input, context={
            'user': context.user,
            'receiving_person_id': formatted_input.get('receiving_person_id')
        })
        serializer.is_valid(raise_exception=True)

        product = Product.objects.get(pk=formatted_input.get('product_id'))
        associated_event = AssociatedEvent.objects.get(pk=formatted_input.get('associated_event_id'))
        transaction = Transaction(
            **formatted_input,
            associated_event_date=associated_event.event.next_date,
            cost_usd=product.cost_usd,
            user=context.user)
        transaction.save()
        if settings.TESTING:
            mock_create_stripe_charge(
                user=context.user,
                transaction=transaction,
                request=context
            )
        else:
            create_stripe_charge(
                user=context.user,
                transaction=transaction,
                request=context
            )
        return CreateTransaction(transaction=transaction)
