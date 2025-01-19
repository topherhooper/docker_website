from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
import pytest
from main import app, get_chatgpt, verify_token

class MockChatGPT:
    def __init__(self):
        self.conversation_history = []
        self.get_response = AsyncMock(return_value="Mock response")

@pytest.fixture
def mock_chatgpt():
    return MockChatGPT()

@pytest.fixture
def client(mock_chatgpt):
    app.dependency_overrides[get_chatgpt] = lambda: mock_chatgpt
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
def mock_verify_token():
    # Create a mock that returns a successful verification
    async def mock_verify():
        return {"valid": True, "user_id": "123"}
    
    # Override the verify_token dependency
    app.dependency_overrides[verify_token] = mock_verify
    yield mock_verify
    # Clean up after test
    if verify_token in app.dependency_overrides:
        del app.dependency_overrides[verify_token]

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_chat_without_auth(client):
    response = client.post("/chat", json={"message": "test"})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_verify_token_invalid():
    with TestClient(app) as client:
        response = client.post(
            "/verify_token",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

def test_chat_with_valid_auth(client, mock_chatgpt, mock_verify_token):
    response = client.post(
        "/chat",
        json={"message": "test message"},
        headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 200, response.json()
