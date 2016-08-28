
from graphene import relay, ObjectType, Mutation, String, Field
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from .models import User


class UserNode(DjangoNode):
    class Meta:
        model = User
        filter_fields = ['first_name', 'last_name', 'email']
        filter_order_by = ['first_name', 'last_name', 'email']


class Query(ObjectType):
    user = relay.NodeField(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    class Meta:
        abstract = True


class CreateUser(Mutation):
    class Input:
        username = String()
        first_name = String()
        last_name = String()
        password = String()

    user = Field('UserNode')

    @classmethod
    def mutate(cls, instance, args, info):
        user = User(**args)
        password = args.get('password')
        if password:
            user.set_password(password)
        user.full_clean()
        user.save()
        return CreateUser(user=user)

class Mutation(ObjectType):
    create_user = Field(CreateUser)
