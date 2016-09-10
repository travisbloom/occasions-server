import graphene

import people.schema
import events.schema
import transactions.schema
import products.schema
import locations.schema


class Query(
    people.schema.Query,
    events.schema.Query,
    products.schema.Query,
    transactions.schema.Query,
    locations.schema.Query
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(
    # people.schema.Mutation,
    transactions.schema.Mutation,
    # events.schema.EventMutation,
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(
    name='Occasions Schema',
    node=graphene.relay.NodeField(),
    query=Query,
    mutation=Mutation
)
