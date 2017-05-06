import logging

import rest_framework
from graphene_django.views import GraphQLView
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_social_oauth2.authentication import SocialAuthentication

from common.errors import GQLErrorHandler

logger = logging.getLogger('occasions')


class OccasionsGraphQLView(GraphQLView):

    def format_error(self, error):
        """Override format error, useful for showing the entire stack trace when in development"""
        return GQLErrorHandler(self).format_error(error)

    def can_display_graphiql(self, request, data):
        if request.user.is_superuser or request.user.is_staff:
            return super().can_display_graphiql(request, data)
        else:
            return False

    def parse_body(self, request):
        if isinstance(request, rest_framework.request.Request):
            return request.data
        return super().parse_body(request)

    @classmethod
    def wrap_as_django_rest_framework_view(cls, *args, **kwargs):
        view = cls.as_view(*args, **kwargs)
        view = permission_classes((IsAuthenticated,))(view)
        view = authentication_classes((
            SessionAuthentication,
            OAuth2Authentication,
            SocialAuthentication,
        ))(view)
        view = api_view(['POST', 'GET'])(view)
        return view
