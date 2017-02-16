import django_filters

from .models import Product
from events.models import EventType


class ProductFilter(django_filters.FilterSet):
    info_icontains = django_filters.MethodFilter()
    event = django_filters.CharField(method='filter_event')

    def filter_event(self, queryset, name, value):
        event_types = EventType.filter(events__in=[value]).values_list('id')
        return (
            queryset
            .filter(
                Q(event_id=value) |
                Q(event_types__in=event_types) |
            )
            .ordering('-event_id')
        )

    def filter_info_icontains(self, queryset, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )

    class Meta:
        model = Product
