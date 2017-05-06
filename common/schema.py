from graphene import Schema, ObjectType, Field, String

from common.relay import Node
from events.mutations import EventMutations
from events.types import EventQueries
from locations.mutations.create_associated_location import LocationsMutations
from locations.types import LocationQueries
from people.mutations import CreateUser, PeopleMutations
from people.types import PeopleQueries, UserNode
from products.types import ProductQueries
from transactions.mutations import TransactionMutations
from transactions.types import TransactionQueries


class Query(
    TransactionQueries,
    PeopleQueries,
    EventQueries,
    ProductQueries,
    LocationQueries,
    ObjectType
):
    node = Node.Field()
    current_user = Field(UserNode)

    def resolve_current_user(self, args, context, info):
        return context.user


class Mutation(
    TransactionMutations,
    LocationsMutations,
    EventMutations,
    PeopleMutations,
    ObjectType
):
    pass

schema = Schema(
    query=Query,
    mutation=Mutation
)


class PublicQuery(ObjectType):
    current_user = String()

    def resolve_current_user(self, args, context, info):
        return None


class PublicMutation(ObjectType):
    create_user = CreateUser.Field()


public_schema = Schema(
    query=PublicQuery,
    mutation=PublicMutation
)
