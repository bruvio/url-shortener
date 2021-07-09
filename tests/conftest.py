import pytest
from src.app import app as flask_app


@pytest.fixture(scope="module")
def app():
    yield flask_app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
