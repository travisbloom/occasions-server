from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from .schema import schema
from .views import OccasionsGraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^graphql', OccasionsGraphQLView.wrap_as_django_rest_framework_view(graphiql=True, schema=schema)),
    url(r'^public_graphql', OccasionsGraphQLView.as_view(schema=schema)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
