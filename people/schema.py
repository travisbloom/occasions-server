import django_filters
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login

from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from rest_framework import serializers

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


class CreateUserInputSerializers(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(validators=[validate_password])


class CreateUser(relay.ClientIDMutation):

    class Input:
        username = String(required=True)
        password = String(required=True)

    user = Field(lambda: UserNode)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        serializer = CreateUserInputSerializers(data=input)
        serializer.is_valid()
        if not serializer.is_valid():
            raise Exception(serializer.errors)

        user = User(username=User.objects.normalize_email(input.get('username')))
        user.set_password(input.get('password'))
        user.save()
        login(context, user, backend='rest_framework_social_oauth2.backends.DjangoOAuth2')

        return CreateUser(user=user)


class Mutation(AbstractType):
    create_user = CreateUser.Field()
