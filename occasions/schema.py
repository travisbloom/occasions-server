import graphene

import people.schema


class Query(people.schema.Query):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(people.schema.Mutation):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(
    name='Occasions Schema',
    node=graphene.relay.NodeField(),
    query=Query,
    mutation=Mutation
)
