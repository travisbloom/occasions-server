from __future__ import absolute_import

from functools import wraps

from django.http import HttpRequest
from django.conf import settings

from ratelimit import ALL, UNSAFE
from ratelimit.exceptions import Ratelimited
from ratelimit.utils import is_ratelimited


def ratelimit_gql(group=None, key=None, rate=None, method=ALL, block=False):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(cls, input, request, info):
            if not settings.DEBUG:
                request.limited = getattr(request, 'limited', False)
                ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                             key=key, rate=rate, method=method,
                                             increment=True)
                if ratelimited and block:
                    raise Ratelimited('Internal server issues.')
            return fn(cls, input, request, info)
        return _wrapped
    return decorator


ratelimit_gql.ALL = ALL
ratelimit_gql.UNSAFE = UNSAFE
