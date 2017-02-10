from graphene import ID, AbstractType

class AbstractModelType(AbstractType):
    pk = ID()
