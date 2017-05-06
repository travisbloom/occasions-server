from graphene import relay, String, Field
from transactions.test import logger

from common.exceptions import MutationException
from people.types import UserNode
from transactions.stripe import create_stripe_user


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