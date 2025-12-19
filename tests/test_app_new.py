import pytest
from types import SimpleNamespace
from main import create_app


def test_homepage_status_code():
    cfg = SimpleNamespace(TESTING=True, WTF_CSRF_ENABLED=False, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
    app = create_app(cfg)
    client = app.test_client()

    res = client.get('/')
    assert res.status_code == 200
