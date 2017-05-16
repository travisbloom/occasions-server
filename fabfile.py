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
        'event_dates',
        'associated_events',

        # transactions
        'transactions'
    ]

    local('./manage.py loaddata {}'.format(' '.join(fixtures_order)))


def bootstrap_db():
    local('rm db.sqlite3')
    local('./manage.py migrate')
    local('./manage.py loaddata users')
    local('fab fixtures')
    local('./manage.py changepassword travisbloom@gmail.com')
    local('./manage.py build_mock_oauth_provider')
