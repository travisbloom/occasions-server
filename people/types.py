from datetime import datetime

from graphene import String, Field, AbstractType, Boolean, Connection
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from oauth2_provider.models import AccessToken

from common.gql.types import AbstractModelType
from common.relay import Node
from .filters import PersonFilter, RelationshipTypeFilter
from .models import User, Person, Relationship, RelationshipType


class AccessTokenNode(AbstractModelType, DjangoObjectType):

    class Meta:
        interfaces = (Node, )
        model = AccessToken
        only_fields = (
            'expires',
            'token'
        )


class RelationshipTypeNode(AbstractModelType, DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = RelationshipType
        only_fields = ()


class RelationshipNode(AbstractModelType, DjangoObjectType):

    class Meta:
        interfaces = (Node, )
        model = Relationship
        only_fields = (
            'to_person',
            'from_person',
            'relationship_type'
        )


class PersonFromRelationshipsConnection(Connection):
    class Meta:
        node = RelationshipNode

    class Edge:
        relation = String()

        def resolve_relation(self, *args):
            return self.node.to_person_name(
                self.node.to_person,
                self.node.relationship_type
            )


class PersonNode(AbstractModelType, DjangoObjectType):
    from_relationships = DjangoFilterConnectionField(
        PersonFromRelationshipsConnection
    )
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
            'transactions',
        )

    def resolve_related_people(self, args, context, info):
        return Person.objects.filter(to_relationships__from_person=self.pk)

    def resolve_has_stripe_user(self, args, context, info):
        return bool(self.stripe_user_id)

    def resolve_access_token(self, args, context, info):
        return self.accesstoken_set.filter(
            expires__gt=datetime.now()).order_by('-expires').first()


class PeopleQueries(AbstractType):
    users = DjangoFilterConnectionField(UserNode)
    people = DjangoFilterConnectionField(
        PersonNode,
        filterset_class=PersonFilter
    )
    relationships = DjangoFilterConnectionField(RelationshipNode)
    relationship_types = DjangoFilterConnectionField(
        RelationshipTypeNode,
        filterset_class=RelationshipTypeFilter
    )

