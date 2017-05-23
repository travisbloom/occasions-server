from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from events.admin_views.associated_event_autocomplete import AssociatedEventAutocomplete
from locations.admin_views.locations.associated_location_autocomplete import AssociatedLocationAutocomplete
from people.admin_views.person_autocomplete import PersonAutocomplete
from people.admin_views.user_autocomplete import UserAutocomplete
from .schema import schema
from .views import OccasionsGraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'admin_autocomplete/person',
        PersonAutocomplete.as_view(),
        name='admin_autocomplete_person'
        ),
    url(r'admin_autocomplete/user',
        UserAutocomplete.as_view(),
        name='admin_autocomplete_user'
        ),
    url(r'admin_autocomplete/associated_event',
        AssociatedEventAutocomplete.as_view(),
        name='admin_autocomplete_associated_event'
        ),
    url(r'admin_autocomplete/associated_location',
        AssociatedLocationAutocomplete.as_view(),
        name='admin_autocomplete_associated_location'
        ),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^graphql', OccasionsGraphQLView.wrap_as_django_rest_framework_view(graphiql=True, schema=schema)),
    url(r'^public_graphql', OccasionsGraphQLView.as_view(schema=schema)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
