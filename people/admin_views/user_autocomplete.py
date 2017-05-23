from dal import autocomplete

from common.utils.search import build_search_filters
from people.models import User


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return False
        return User.objects.filter(build_search_filters(
            self.q,
            ('first_name__icontains', 'last_name__icontains'),
            ('id',)
        ))
