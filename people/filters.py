import django_filters

from .models import Person


class PersonFilter(django_filters.FilterSet):
    info_icontains = django_filters.MethodFilter()

    def filter_info_icontains(self, queryset, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )

    class Meta:
        model = Person
        fields = ['info_icontains']
