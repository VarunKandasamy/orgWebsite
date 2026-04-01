import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def client():
    """Session-scoped test client — app starts once for the whole suite."""
    with TestClient(app, follow_redirects=False) as c:
        yield c


@pytest.fixture(scope="session")
def client_follow(client):
    """Convenience: a client that follows redirects, for checking final pages."""
    with TestClient(app, follow_redirects=True) as c:
        yield c
