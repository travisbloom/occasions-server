from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from graphene import relay, String, Field
from rest_framework import serializers

from common.exceptions import FormValuesException
from common.gql.ratelimit import ratelimit_gql
from people.models import User
from people.types import UserNode


class CreateUserInputSerializers(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(validators=[validate_password])


class CreateUser(relay.ClientIDMutation):

    class Input:
        username = String(required=True)
        password = String(required=True)

    user = Field(UserNode)

    @classmethod
    @ratelimit_gql(key='ip', rate='20/m', block=True)
    def mutate_and_get_payload(cls, input, context, info):
        serializer = CreateUserInputSerializers(data=input)
        serializer.is_valid()
        if not serializer.is_valid():
            raise FormValuesException(serializer.errors)
        try:
            user = User(
                username=User.objects.normalize_email(
                    input.get('username')))
            user.set_password(input.get('password'))
            user.save()
        except IntegrityError:
            raise FormValuesException(
                {'username': 'A user with this information already exists'})

        return CreateUser(user=user)
