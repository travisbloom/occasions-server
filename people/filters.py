import django_filters
from django.db.models import Q

from .models import Person, RelationshipType


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


class RelationshipTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = RelationshipType
        fields = (
            'search',
        )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(from_person_male_display_name__icontains=value) |
            Q(from_person_female_display_name__icontains=value) |
            Q(to_person_male_display_name__icontains=value) |
            Q(to_person_female_display_name__icontains=value)
        )



