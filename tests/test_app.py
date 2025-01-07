from app import app
import pytest


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_load_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data