import traceback

from django.conf import settings
from graphql import GraphQLError
from rest_framework.exceptions import PermissionDenied, ValidationError

from common.utils.camelcase import camelize

GENERIC_MESSAGE = 'Whoops! Something went wrong on our end. We\'re looking in to it now.'


class ResourceDoesNotExist(Exception):
    pass


class GQLErrorHandler:
    """Utlity class which centralizes GraphQL error formatting"""

    def __init__(self, view):
        self.view = view

    def format_error(self, error):
        err = error.original_error if hasattr(error, 'original_error') else error
        original_message = str(error)
        result = {
            'message': original_message,
            'stack': traceback.format_tb(err.__traceback__)
        }
        if isinstance(error, GraphQLError):
            original_message = error.message
            result['message'] = original_message
            if error.locations is not None:
                result['locations'] = [{'line': loc.line, 'column': loc.column} for loc in error.locations]
        try:
            raise err
        except ValidationError as e:
            result['data'] = camelize(e.detail)
        except ResourceDoesNotExist:
            pass
        except PermissionDenied:
            pass
        except Exception:
            result['message'] = GENERIC_MESSAGE

        if self.should_remove_stack():
            if 'stack' in result:
                del result['stack']
            if 'locations' in result:
                del result['locations']
        else:
            result['message'] = original_message

        return result

    def should_remove_stack(self):
        """We should add the stack if the test cases is not expected to be an error"""
        return not settings.ENVIRONMENT == 'local' and not settings.TESTING