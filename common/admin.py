from dal import autocomplete
from django.contrib import admin

from events.models import AssociatedEvent
from locations.models import AssociatedLocation
from people.models import Person, User


class BaseModelAdmin(admin.ModelAdmin):
    search_fields = (
        '=id',
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.remote_field.model == Person:
            kwargs['widget'] = autocomplete.ModelSelect2(
                url='admin_autocomplete_person',
                forward=('user',)
            )
        elif db_field.remote_field.model == User:
            kwargs['widget'] = autocomplete.ModelSelect2(url='admin_autocomplete_user')
        elif db_field.remote_field.model == AssociatedEvent:
            kwargs['widget'] = autocomplete.ModelSelect2(
                url='admin_autocomplete_associated_event',
                forward=('receiving_person',)
            )
        elif db_field.remote_field.model == AssociatedLocation:
            kwargs['widget'] = autocomplete.ModelSelect2(
                url='admin_autocomplete_associated_location',
                forward=('receiving_person',)
            )
        return super(BaseModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
