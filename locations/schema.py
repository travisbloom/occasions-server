from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from .models import Location, PersonLocation


class LocationNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = Location


class PersonLocationNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PersonLocation
        filter_fields = ['person']


class Query(AbstractType):
    location = relay.Node.Field(LocationNode)
    locations = DjangoFilterConnectionField(LocationNode)

    person_location = relay.Node.Field(PersonLocationNode)
    person_locations = DjangoFilterConnectionField(PersonLocationNode)
