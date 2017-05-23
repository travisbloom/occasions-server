from dal import autocomplete

from common.utils.search import build_search_filters
from events.models import AssociatedEvent


class AssociatedEventAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return False
        qs = AssociatedEvent.objects.filter(build_search_filters(
            self.q,
            ('event__name',),
            ('id',)
        ))
        if self.forwarded.get('receiving_person', None):
            qs = qs.filter(receiving_person_id=self.forwarded.get('receiving_person', None))
        return qs
