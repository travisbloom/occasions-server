from fabric.api import local


def bootstrap_db():
    local('rm db.sqlite3')
    local('./manage.py migrate')
    local('./manage.py bootstrap_mock_data')
