from typing import Optional
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

class ChatGPT:
    SYSTEM_PROMPT = """You are a story teller that tells aesop-like fables. You rarely answer things directly, but instead try to answer with a story or fable."""

    def __init__(self, client: Optional[OpenAI] = None):
        if client is None:
            # Load environment variables from .credentials directory
            credentials_path = Path(__file__).parents[1] / '.credentials' / 'openai.env'
            load_dotenv(credentials_path)
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.client = client
        self.conversation_history = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]

    async def get_response(self, message: str) -> str:
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Get response using full conversation history
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.conversation_history
        )
        
        # Add assistant's response to history
        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant", 
            "content": assistant_message
        })
        
        return assistant_message