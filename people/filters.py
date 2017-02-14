import django_filters
from django.db.models import Q

from .models import Person


class PersonFilter(django_filters.FilterSet):
    info_contains = django_filters.CharFilter(method='filter_info_contains')

    class Meta:
        model = Person
        fields = (
            'info_contains',
        )


    def filter_info_contains(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )
