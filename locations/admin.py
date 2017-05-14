from django.contrib import admin

from common.admin import BaseModelAdmin
from locations.models import AssociatedLocation, Location


@admin.register(Location)
class LocationAdmin(BaseModelAdmin):
    search_fields = (
        'city',
        'state',
        'country',
        '=id',
    )


@admin.register(AssociatedLocation)
class AssociatedLocationAdmin(BaseModelAdmin):
    search_fields = (
        'location__city',
        'location__state',
        'location__country',
        'person__first_name',
        'person__last_name',
        '=id',
    )
