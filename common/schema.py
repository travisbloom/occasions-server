from graphene import Schema, ObjectType, Field

from common.relay import Node
from events.mutations import EventMutations
from events.types import EventStaffQueries, EventQueries
from locations.mutations.create_associated_location import LocationsMutations
from locations.types import LocationStaffQueries
from people.mutations import CreateUser, PeopleMutations
from people.types import PeopleStaffQueries, UserNode, PeopleQueries
from products.types import ProductQueries
from transactions.mutations import TransactionMutations
from transactions.types import TransactionStaffQueries


class StaffType(
    TransactionStaffQueries,
    PeopleStaffQueries,
    EventStaffQueries,
    LocationStaffQueries,
    ObjectType
):
    pass


class Query(
    PeopleQueries,
    EventQueries,
    ProductQueries,
    ObjectType
):
    node = Node.Field()
    current_user = Field(UserNode)
    staff = Field(StaffType)

    def resolve_current_user(self, args, context, info):
        return context.user

    def resolve_staff(self, args, context, info):
        return args


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
    current_user = Field(UserNode)

    def resolve_current_user(self, args, context, info):
        return None


class PublicMutation(ObjectType):
    create_user = CreateUser.Field()


public_schema = Schema(
    query=PublicQuery,
    mutation=PublicMutation
)
