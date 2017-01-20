import django_filters
from django.db.models import Q

from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from .models import User, Person, Relationship


class UserNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = User


class PersonFilter(django_filters.FilterSet):
    info_icontains = django_filters.MethodFilter()

    def filter_info_icontains(self, queryset, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )

    class Meta:
        model = Person
        fields = ['info_icontains']


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


class CreateUser(relay.ClientIDMutation):

    class Input:
        username = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)
        password = String(required=True)

    user = Field(lambda: UserNode)

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        user = User(
            first_name=input.get('first_name'),
            last_name=input.get('last_name'),
            username=input.get('username'),
        )
        password = input.get('password')
        if password:
            user.set_password(password)
        user.full_clean()
        user.save()
        return CreateUser(user=user)


class Mutation(AbstractType):
    create_user = CreateUser.Field()
