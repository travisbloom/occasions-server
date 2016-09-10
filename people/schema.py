import django_filters
from django.db.models import Q

from graphene import relay, ObjectType, Mutation, String, Field
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from .models import User, Person, Relationship


class UserNode(DjangoNode):
    class Meta:
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


class PersonNode(DjangoNode):
    class Meta:
        model = Person


class RelationshipNode(DjangoNode):
    class Meta:
        model = Relationship


class Query(ObjectType):
    user = relay.NodeField(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    person = relay.NodeField(PersonNode)
    people = DjangoFilterConnectionField(PersonNode, filterset_class=PersonFilter)

    relationship = relay.NodeField(RelationshipNode)
    relationships = DjangoFilterConnectionField(RelationshipNode)

    class Meta:
        abstract = True


class CreateUser(relay.ClientIDMutation):

    class Input:
        username = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)
        password = String(required=True)

    user = Field('UserNode')

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


class Mutation(ObjectType):
    create_user = Field(CreateUser)
