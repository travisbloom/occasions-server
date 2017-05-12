import django_filters
from django.db.models import Q

from .models import Person


class PersonFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Person
        fields = (
            'search',
        )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )



