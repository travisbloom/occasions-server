from graphene import AbstractType

from people.mutations.create_person import CreatePerson
from people.mutations.create_user import CreateUser

class PeopleMutations(AbstractType):
    create_user = CreateUser.Field()
    create_person = CreatePerson.Field()