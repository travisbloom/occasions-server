from django.db.models import Q


def build_search_filters(value, filter_exp=None, numeric_filter_exp=None):
    filters = Q()
    for word in value.split():
        new_filter_group = Q()
        if filter_exp:
            for exp in filter_exp:
                new_filter_group = new_filter_group | Q(**{exp: word})
        if numeric_filter_exp and word.isnumeric():
            for exp in numeric_filter_exp:
                new_filter_group = new_filter_group | Q(**{exp: word})
        filters = filters & new_filter_group
    return filters
