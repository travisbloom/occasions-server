from datetime import datetime
from django.db.models import Q
from oauth2_provider.models import AccessToken
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login

from common.gql.ratelimit import ratelimit_gql

from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from rest_framework import serializers

from .models import User, Person, Relationship
from .filters import PersonFilter


class AccessTokenNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = AccessToken


class UserNode(DjangoObjectType):
    access_tokens = DjangoFilterConnectionField(AccessTokenNode)

    class Meta:
        interfaces = (relay.Node, )
        model = User
        only_fields = (
            'username',
            'isActive',
            'dateJoined',
            'datetimeCreated',
            'datetimeUpdated',
            'person',
        )

    def resolve_access_tokens(self, args, context, info):
        return self.accesstoken_set.filter(expires__gt=datetime.now())


class PersonNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = Person


class RelationshipNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = Relationship


class Query(AbstractType):
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    person = relay.Node.Field(PersonNode)
    people = DjangoFilterConnectionField(PersonNode, filterset_class=PersonFilter)

    relationship = relay.Node.Field(RelationshipNode)
    relationships = DjangoFilterConnectionField(RelationshipNode)


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
            raise Exception(serializer.errors)
        try:
            user = User(username=User.objects.normalize_email(input.get('username')))
            user.set_password(input.get('password'))
            user.save()
        except IntegrityError:
            raise Exception({'username': 'A user with this information already exists'})

        login(context, user, backend='rest_framework_social_oauth2.backends.DjangoOAuth2')
        return CreateUser(user=user)


class Mutation(AbstractType):
    create_user = CreateUser.Field()
