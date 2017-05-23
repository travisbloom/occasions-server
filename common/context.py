from django.utils.functional import cached_property

from events.loaders.associated_event import AssociatedEventLoader
from events.loaders.event import EventLoader
from events.loaders.event_date import EventDateByEventLoader, NextEventDateByEventLoader, EventDateLoader
from events.loaders.event_type import EventTypesByEventLoader, EventTypesByProductLoader
from locations.loaders.associated_location import AssociatedLocationLoader
from locations.loaders.location import LocationLoader
from people.loaders.person import PersonLoader
from people.loaders.relationship import RelationshipLoader, FromRelationshipByPersonLoader
from people.loaders.relationship_type import RelationshipTypeLoader


class Context(object):
    def __init__(self, req=None):
        self._req = req
        self.META = req.META

    @property
    def user(self):
        return self._req.user

    @cached_property
    def person_loader(self):
        return PersonLoader()

    @cached_property
    def relationship_loader(self):
        return RelationshipLoader()

    @cached_property
    def from_relationship_by_person_loader(self):
        return FromRelationshipByPersonLoader()

    @cached_property
    def relationship_type_loader(self):
        return RelationshipTypeLoader()

    @cached_property
    def event_loader(self):
        return EventLoader()

    @cached_property
    def associated_event_loader(self):
        return AssociatedEventLoader()

    @cached_property
    def event_date_loader(self):
        return EventDateLoader()

    @cached_property
    def event_date_by_event_loader(self):
        return EventDateByEventLoader()

    @cached_property
    def next_event_date_by_event_loader(self):
        return NextEventDateByEventLoader()

    @cached_property
    def event_types_by_event_loader(self):
        return EventTypesByEventLoader()

    @cached_property
    def event_types_by_product_loader(self):
        return EventTypesByProductLoader()

    @cached_property
    def location_loader(self):
        return LocationLoader()

    @cached_property
    def associated_location_loader(self):
        return AssociatedLocationLoader()
