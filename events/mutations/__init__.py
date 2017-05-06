from graphene import AbstractType

from .create_associated_event import CreateAssociatedEvent


class EventMutations(AbstractType):
    create_associated_event = CreateAssociatedEvent.Field()
