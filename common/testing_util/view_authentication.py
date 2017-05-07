from rest_framework.authentication import BaseAuthentication

from people.models import User


class MockUserLoginAuthentication(BaseAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """
        return (User.objects.get(pk=1), None)
