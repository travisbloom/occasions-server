from datetime import datetime
from django.db.models import Q
from oauth2_provider.models import AccessToken
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login

from common.gql.ratelimit import ratelimit_gql

from graphene import relay, ObjectType, Mutation, String, Field, AbstractType, ID, Boolean
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from rest_framework import serializers

from common.exceptions import FormValuesException
from common.gql.types import AbstractModelType

from people.models import User, Person, Relationship
from people.filters import PersonFilter
from people.schema import UserNode


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
