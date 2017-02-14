from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoConnectionField

class DjangoModelConnectionField(DjangoFilterConnectionField):
    @staticmethod
    def connection_resolver(resolver, connection, default_manager, filterset_class, filtering_args,
                            root, args, context, info):
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = default_manager.get_queryset()
        qs = filterset_class(data=filter_kwargs, queryset=qs).qs
        # pass the qs down to the child resolver
        return DjangoConnectionField.connection_resolver(
            resolver,
            connection,
            qs,
            root,
            args,
            context,
            info
            )
