from graphene import relay, ObjectType, Mutation, String, Field, AbstractType, Argument, ID
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType

from .models import Product


class ProductNode(DjangoObjectType):
    slug = ID(source='pk')
    class Meta:
        interfaces = (relay.Node, )
        model = Product


class Query(AbstractType):
    product = Field(ProductNode, slug=Argument(ID), id=Argument(ID))
    products = DjangoFilterConnectionField(ProductNode)

    def resolve_product(self, args, context, info):
        if args.get('id'):
            return relay.Node.node_resolver(self, args, context, info)
        return Product.objects.get(id=args.get('slug'))
