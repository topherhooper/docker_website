import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_chat_without_auth(client):
    response = client.post("/chat", json={"message": "test"})
    assert response.status_code == 403  # Unauthorized

@pytest.mark.asyncio
async def test_verify_token_invalid():
    with TestClient(app) as client:
        response = client.post(
            "/verify_token",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401