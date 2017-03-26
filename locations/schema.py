from graphene import relay, ObjectType, Mutation, String, Field, AbstractType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from common.gql.types import AbstractModelType
from common.relay import Node
from .models import Location, AssociatedLocation


class LocationNode(AbstractModelType, DjangoObjectType):
    display_name = String()

    class Meta:
        interfaces = (Node, )
        model = Location

    def resolve_display_name(self, args, context, info):
        return "{street_address_line1}{street_address_line2}, {city} {state} {postal_code}".format(
            street_address_line1=self.street_address_line1,
            street_address_line2=" {}".format(
                self.street_address_line2) if self.street_address_line2 else "",
            city=self.city,
            state=self.state,
            postal_code=self.postal_code)


class AssociatedLocationNode(AbstractModelType, DjangoObjectType):

    class Meta:
        interfaces = (Node, )
        model = AssociatedLocation
        filter_fields = ['person']


class Query(AbstractType):
    locations = DjangoFilterConnectionField(LocationNode)
    person_locations = DjangoFilterConnectionField(AssociatedLocationNode)
