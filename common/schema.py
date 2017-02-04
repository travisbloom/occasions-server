from graphene import relay, Schema, ObjectType, Field
import people.schema
import events.schema
import transactions.schema
import products.schema
import locations.schema


class Query(
    transactions.schema.Query,
    people.schema.Query,
    events.schema.Query,
    products.schema.Query,
    locations.schema.Query,
    ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    node=relay.Node,
    current_user=Field(people.schema.UserNode)

    def resolve_current_user(self, args, context, info):
        return context.user


class Mutation(
    people.schema.Mutation,
    transactions.schema.Mutation,
    events.schema.Mutation,
    ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = Schema(
    query=Query,
    mutation=Mutation
)