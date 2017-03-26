from graphene import AbstractType, Field
from .create_associated_event import CreateAssociatedEvent


class EventsMutation(AbstractType):
    create_associated_event = CreateAssociatedEvent.Field()
