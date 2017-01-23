from graphene_django.views import GraphQLView
from graphql.error import GraphQLError


class OccasionsGraphQLView(GraphQLView):

    def format_error(self, error):
        """Override format error, useful for showing the entire stack trace when in development"""
        if not isinstance(error, GraphQLError):
            return {'message': error}

        formatted_error = {'message': error.message}
        if error.locations is not None:
            formatted_error['locations'] = [
                {'line': loc.line, 'column': loc.column}
                for loc in error.locations
            ]
        try:
            formatted_error['data'] = error.original_error.args[0]
        except Exception:
            pass

        return formatted_error
