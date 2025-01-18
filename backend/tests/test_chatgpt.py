import pytest
from unittest.mock import MagicMock
from chatgpt import ChatGPT

@pytest.fixture
def mock_client():
    client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Test response"))
    ]
    client.chat.completions.create.return_value = mock_response
    return client

@pytest.fixture
def chatgpt(mock_client):
    # Inject the mock client directly
    return ChatGPT(client=mock_client)

@pytest.mark.asyncio
async def test_get_response(chatgpt, mock_client):
    response = await chatgpt.get_response("Test message")
    
    assert response == "Test response"
    
    # Verify the correct call was made
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=[
            {"role": "system", "content": ChatGPT.SYSTEM_PROMPT},
            {"role": "user", "content": "Test message"},
            {"role": "assistant", "content": "Test response"}
        ]
    )

@pytest.mark.asyncio
async def test_conversation_history_updated(chatgpt):
    await chatgpt.get_response("Test message")
    
    history = chatgpt.conversation_history
    assert len(history) == 3  # system + user + assistant
    assert history[0] == {"role": "system", "content": ChatGPT.SYSTEM_PROMPT}
    assert history[1] == {"role": "user", "content": "Test message"}
    assert history[2] == {"role": "assistant", "content": "Test response"}