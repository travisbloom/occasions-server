from graphene import relay, ObjectType
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from .models import User


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
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
