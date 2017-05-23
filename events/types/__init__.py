from graphene import AbstractType, ID, List
from graphene_django.filter import DjangoFilterConnectionField

from events.filters import EventFilter, EventTypeFilter
from events.models import Event
from events.types.associated_event import AssociatedEventNode
from events.types.event import EventNode
from events.types.event_type import EventTypeNode


class EventQueries(AbstractType):
    event_types = DjangoFilterConnectionField(
        EventTypeNode, filterset_class=EventTypeFilter)
    default_events = DjangoFilterConnectionField(
        EventNode,
        filterset_class=EventFilter,
        event_types_pk_in=List(ID)
    )

    def resolve_default_events(self, args, context, info):
        return Event.objects.filter(is_default_event=True)


class EventStaffQueries(AbstractType):
    associated_events = DjangoFilterConnectionField(AssociatedEventNode)
    events = DjangoFilterConnectionField(
        EventNode,
        filterset_class=EventFilter,
        event_types_pk_in=List(ID)
    )
