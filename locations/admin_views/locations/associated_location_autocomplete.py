from dal import autocomplete

from common.utils.search import build_search_filters
from locations.models import AssociatedLocation


class AssociatedLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return False
        qs = AssociatedLocation.objects.filter(build_search_filters(
            self.q,
            ('location__city', 'location__country', 'location__state'),
            ('id',)
        ))
        if self.forwarded.get('receiving_person', None):
            qs = qs.filter(person_id=self.forwarded.get('receiving_person', None))
        return qs