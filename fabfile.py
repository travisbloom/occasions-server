from fabric.api import local

def fixtures():
    """Loads all the fixtures in every dir"""
    fixtures_order = [
        # people
        'users',
        'people',
        'relationships',

        # locations
        'locations',
        'person_locations',

        # products
        'products',

        # events
        'events',
        'associated_events',

        # transactions
        'transactions'
    ]

    local('./manage.py loaddata {}'.format(' '.join(fixtures_order)))
