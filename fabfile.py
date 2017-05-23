from fabric.api import local


def reset_migrations():
    local('rm db.sqlite3')
    for dir in ['events', 'locations', 'people', 'transactions', 'products']:
        local('rm -rf {}/migrations/'.format(dir))
        local('mkdir {}/migrations/'.format(dir))
        local('touch {}/migrations/__init__.py'.format(dir))
    local('./manage.py makemigrations')


def bootstrap_db():
    local('rm db.sqlite3')
    local('./manage.py migrate')
    local('./manage.py bootstrap_mock_data')
    local('./manage.py generate_events_next_date')
