from django.contrib import admin
from django.urls import reverse

from common import settings
from common.admin import BaseModelAdmin
from common.relay import Node
from transactions.models import Transaction
from transactions.types import TransactionNode


def user(transaction):
    return transaction.user.full_name
user.short_description = 'User'
user.admin_order_field = 'user__person__first_name'

def receiving_person(transaction):
    return transaction.receiving_person.full_name
receiving_person.short_description = 'Receiving Person'
receiving_person.admin_order_field = 'receiving_person__first_name'


def event(transaction):
    return transaction.associated_event.event.name
event.short_description = 'Event'
event.admin_order_field = 'associated_event__event__name'


@admin.register(Transaction)
class TransactionAdmin(BaseModelAdmin):
    search_fields = (
        'user__person__first_name',
        'user__person__last_name',
        'receiving_person__first_name',
        'receiving_person__last_name',
        'associated_event__event__name',
        '=stripe_transaction_id',
        '=id',
    )
    list_filter = (
        'datetime_created',
        'datetime_updated',
    )
    list_display = (
        user,
        receiving_person,
        event,
        'datetime_created',
        'datetime_updated',
        'id'
    )
    list_select_related = (
        'user',
        'user__person',
        'receiving_person',
        'associated_event',
        'associated_event__event'
    )

    def view_on_site(self, obj):
        return "{}a/yourGifts/{}".format(
            settings.APP_URL,
            Node.to_global_id(TransactionNode.__name__, obj.pk)
        )

