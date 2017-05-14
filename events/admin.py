from django.contrib import admin

from common.admin import BaseModelAdmin
from events.models import EventType, Event


@admin.register(EventType)
class EventTypeAdmin(BaseModelAdmin):
    search_fields = (
        'display_name',
        '=name',
    )
    list_display = (
        'display_name',
        'name',
    )
    prepopulated_fields = {'name': ('display_name',)}


@admin.register(Event)
class EventAdmin(BaseModelAdmin):
    filter_horizontal = ('event_types',)
    search_fields = (
        'event_types__display_name',
        'name',
        '=id',
    )
    list_display = (
        'name',
        'id',
        'is_default_event'
    )
