from django.contrib import admin

from common.admin import BaseModelAdmin
from products.models import Product


def related_event(product):
    return product.event.name if product.event else None
related_event.short_description = 'Related Event'


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    filter_horizontal = ('event_types',)
    search_fields = (
        'name',
        'event_types__display_name',
        'event__name',
        '=id',
    )
    list_display = (
        'name',
        'description',
        related_event,
        'id'
    )
    prepopulated_fields = {'id': ('name',)}
