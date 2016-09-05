import graphene

import people.schema
import events.schema


class Query(people.schema.Query, events.schema.Query):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(
    # people.schema.Mutation,
    events.schema.EventMutation,
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
