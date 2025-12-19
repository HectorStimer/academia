import pytest

from main import create_app


def test_homepage_status_code():
    app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED': False, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    client = app.test_client()

    res = client.get('/')
    assert res.status_code == 200
