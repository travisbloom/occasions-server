from graphene import relay, ObjectType, Mutation, String, Field, AbstractType, ID
from graphene_django.filter import DjangoFilterConnectionField
from common.gql.types import AbstractModelType
from graphene.types.json import JSONString
from rest_framework import serializers
from raven.contrib.django.raven_compat.models import client as raven_client
import logging

from common.exceptions import FormValuesException, MutationException
from people.serializers import PersonWithRelationToCurrentUserField
from people.schema import UserNode
from locations.models import AssociatedLocation
from events.models import AssociatedEvent
from products.models import Product

from .models import Transaction
from .schema import TransactionNode
from .stripe import create_stripe_user, create_strip_charge

logger = logging.getLogger('occasions')


class CreateStripeUser(relay.ClientIDMutation):

    class Input:
        strip_transaction_id = String(required=True)
        email = String(required=True)

    user = Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if context.user.stripe_user_id:
            error_msg = 'User tried to create stripe account that already existed'
            logger.warn(error_msg, extra={'request': context})
            raise MutationException(error_msg)

        create_stripe_user(
            payload={
                **input},
            user=context.user,
            request=context)
        return CreateStripeUser(user=context.user)


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
            logger.warn(error_msg, extra={'request': context})
            raise MutationException(error_msg)

        serializer = CreateTransactionSerializer(data=input, context={
            'user': context.user,
            'receiving_person_id': input.get('receiving_person_id')
        })
        if not serializer.is_valid():
            raise FormValuesException(serializer.errors)

        product = Product.objects.get(pk=input.get('product_id'))
        transaction = Transaction(
            **input,
            cost_usd=product.cost_usd,
            user=context.user)
        transaction.save()
        create_strip_charge(
            user=context.user,
            transaction=transaction,
            request=context
        )
        return CreateTransaction(transaction=transaction)


class TransactionMutation(AbstractType):
    create_transaction = CreateTransaction.Field()
    create_stripe_user = CreateStripeUser.Field()
