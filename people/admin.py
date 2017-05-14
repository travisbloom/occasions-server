from django.contrib import admin

from common.admin import BaseModelAdmin
from .models import User, Person, Relationship


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    search_fields = (
        'username',
        'person__last_name',
        'person__first_name',
        '=id',
    )
    list_display = (
        'username',
        'full_name',
        'id'
    )


@admin.register(Person)
class PersonAdmin(BaseModelAdmin):
    search_fields = (
        'first_name',
        'last_name',
        'email',
        '=id',
    )
    list_display = (
        'full_name',
        'email',
        'id'
    )


# @admin.register(Relationship)
# class RelationshipAdmin(BaseModelAdmin):
#     pass

