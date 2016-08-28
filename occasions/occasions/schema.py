import graphene

import people.schema


class Query(people.schema.Query):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(name='Occasions Schema')
schema.query = Query
