from dal import autocomplete

from common.utils.search import build_search_filters
from people.models import Person


class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return False
        qs = Person.objects.filter(build_search_filters(
            self.q,
            ('first_name__icontains', 'last_name__icontains'),
            ('id',)
        ))
        if self.forwarded.get('user', None):
            qs = qs.filter(to_relationships__from_person__user_id=self.forwarded.get('user', None))
        return qs