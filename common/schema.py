from graphene import relay, Schema, ObjectType, Field

import people.schema
import events.schema
import transactions.schema
import products.schema
import locations.schema

from transactions.mutations import TransactionMutation
from locations.mutations import LocationsMutation
from people.mutations import PeopleMutation, CreateUser


class Query(
    transactions.schema.Query,
    people.schema.Query,
    events.schema.Query,
    products.schema.Query,
    locations.schema.Query,
    ObjectType
):
    node = relay.Node,
    current_user = Field(people.schema.UserNode)

    def resolve_current_user(self, args, context, info):
        return context.user


class Mutation(
    PeopleMutation,
    TransactionMutation,
    events.schema.Mutation,
    LocationsMutation,
    ObjectType
):
    pass

schema = Schema(
    query=Query,
    mutation=Mutation
)


class PublicMutation(ObjectType):
    create_user = CreateUser.Field()

public_schema = Schema(
    mutation=PublicMutation
)
