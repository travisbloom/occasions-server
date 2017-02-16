from fabric.api import local


def fixtures():
    """Loads all the fixtures in every dir"""
    fixtures_order = [
        # people
        'people',
        'relationships',

        # locations
        'locations',
        'associated_locations',

        # products
        'products',

        # events
        'event_types',
        'events',
        'associated_events',

        # transactions
        'transactions'
    ]

    local('./manage.py loaddata {}'.format(' '.join(fixtures_order)))


def bootstrap_db():
    local('./manage.py migrate')
    local('./manage.py loaddata users')
    local('fab fixtures')
    local('./manage.py changepassword travisbloom@gmail.com')
    local('echo "Go to http://127.0.0.1:8000/admin/oauth2_provider/application/add/ and create a new application"')
    local('echo "user should be a superuser"')
    local('echo "redirect_uris should be left blank"')
    local('echo "client_type should be set to confidential"')
    local('echo "authorization_grant_type should be set to Resource owner password-based"')
