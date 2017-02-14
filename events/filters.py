import django_filters
from django.db.models import Q

from .models import Event, EventType


class EventFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Event
        fields = (
            'search',
        )

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))


class EventTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Event
        fields = (
            'search',
        )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(display_name__icontains=value)
        )
