import rest_framework
import logging
import traceback
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework_social_oauth2.authentication import SocialAuthentication
from django.contrib.auth.decorators import login_required

from graphene_django.views import GraphQLView
from graphql.error import GraphQLError

from .exceptions import FormValuesException, StripeException, MutationException
from .utils.camelcase import camelize


logger = logging.getLogger('occasions')


def generic_error_message(formatted_error):
    if not settings.DEBUG:
        formatted_error[
            'message'] = 'Whoops! Something went wrong on our end. We\'re looking in to it now.'
        return formatted_error

    return formatted_error


def format_error_with_debug_info(error):
    formatted_error = {}
    if isinstance(error, GraphQLError):
        formatted_error['message'] = error.message
        if error.locations is not None:
            formatted_error['locations'] = [
                {'line': loc.line, 'column': loc.column}
                for loc in error.locations
            ]

    used_error = error.original_error if hasattr(error, 'original_error') else error
    # formatted_error['stack'] = traceback.format_tb(used_error.__traceback__)
    if isinstance(used_error, FormValuesException):
        formatted_error['data'] = camelize(error.original_error.args[0])
    return formatted_error


class OccasionsGraphQLView(GraphQLView):

    def format_error(self, error):
        """Override format error, useful for showing the entire stack trace when in development"""

        formatted_error = format_error_with_debug_info(error)

        try:
            raise error.original_error if hasattr(error, 'original_error') else error
        except FormValuesException:
            pass
        except Exception as e:
            # FIXME this doesnt give good stacktrace in sentry
            logger.exception('gql error', exc_info=True)

        return formatted_error

    @login_required
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
