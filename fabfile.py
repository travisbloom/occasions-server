from fabric.api import local

def fixtures():
    """Loads all the fixtures in every dir"""
    fixtures_order = [
        # people
        'people',
        'relationships',

        # locations
        'locations',
        'person_locations',

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
