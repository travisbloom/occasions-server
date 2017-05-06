from graphene import AbstractType, ID, List
from graphene_django.filter import DjangoFilterConnectionField

from events.types.associated_event import AssociatedEventNode
from events.types.event import EventNode
from events.types.event_type import EventTypeNode
from events.filters import EventFilter, EventTypeFilter


class EventQueries(AbstractType):
    associated_events = DjangoFilterConnectionField(AssociatedEventNode)
    events = DjangoFilterConnectionField(
        EventNode,
        filterset_class=EventFilter,
        event_types_pk_in=List(ID)
    )
    event_types = DjangoFilterConnectionField(
        EventTypeNode, filterset_class=EventTypeFilter)
