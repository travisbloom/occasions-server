from rest_framework import serializers
from django.db.models import Q
from people.models import Person


class PersonWithRelationToCurrentUserField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        user = self.context['user']
        return Person.objects.filter(
            Q(to_relationships__from_person__user_id=user.id) |
            Q(from_relationships__to_person__user_id=user.id)
        )
