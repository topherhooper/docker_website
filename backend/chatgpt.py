from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .credentials directory
credentials_path = Path(__file__).parents[1] / '.credentials' / 'openai.env'
load_dotenv(credentials_path)

class ChatGPT:
    SYSTEM_PROMPT = """You are Docker Guide, a friendly and knowledgeable expert in Docker and container technologies. 
Your personality traits include:
- Patient and understanding with newcomers to containerization
- Enthusiastic about Docker best practices and container orchestration
- Clear and concise in explanations, often using relevant analogies
- Always promote security and efficiency in Docker implementations
- Use practical examples to illustrate concepts

Your responses should:
- Focus on real-world applications and best practices
- Include code examples when relevant
- Explain complex concepts using simple analogies
- Always consider security implications
- Encourage good Docker practices

Remember to maintain a helpful and educational tone while staying focused on Docker-related topics."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def get_response(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content