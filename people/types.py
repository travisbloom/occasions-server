from datetime import datetime

from graphene import String, Field, AbstractType, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from oauth2_provider.models import AccessToken

from common.gql.types import AbstractModelType
from common.relay import Node
from .filters import PersonFilter
from .models import User, Person, Relationship


class AccessTokenNode(AbstractModelType, DjangoObjectType):

    class Meta:
        interfaces = (Node, )
        model = AccessToken
        only_fields = (
            'expires',
            'token'
        )


class PersonNode(AbstractModelType, DjangoObjectType):
    full_name = String()

    class Meta:
        interfaces = (Node, )
        model = Person


class UserNode(AbstractModelType, DjangoObjectType):
    access_token = Field(AccessTokenNode)
    email = String(source='username')
    has_stripe_user = Boolean()
    related_people = DjangoFilterConnectionField(
        PersonNode, filterset_class=PersonFilter)

    class Meta:
        interfaces = (Node, )
        model = User
        only_fields = (
            'isActive',
            'dateJoined',
            'datetimeCreated',
            'datetimeUpdated',
            'person',
        )

    def resolve_related_people(self, args, context, info):
        return Person.objects.filter(to_relationships__from_person=self.pk)

    def resolve_has_stripe_user(self, args, context, info):
        return bool(self.stripe_user_id)

    def resolve_access_token(self, args, context, info):
        return self.accesstoken_set.filter(
            expires__gt=datetime.now()).order_by('-expires').first()


class RelationshipNode(AbstractModelType, DjangoObjectType):

    class Meta:
        interfaces = (Node, )
        model = Relationship


class PeopleQueries(AbstractType):
    users = DjangoFilterConnectionField(UserNode)
    people = DjangoFilterConnectionField(
        PersonNode, filterset_class=PersonFilter)
    relationships = DjangoFilterConnectionField(RelationshipNode)
