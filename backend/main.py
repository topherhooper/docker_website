from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from chatgpt import ChatGPT
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests
from functools import lru_cache

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173", 
        "https://topherhooper.com",
        "https://chatbot-frontend-614936797883.us-central1.run.app",
        "https://chatbot-backend-614936797883.us-central1.run.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache()
def get_chatgpt():
    return ChatGPT()

security = HTTPBearer()

class ChatMessage(BaseModel):
    message: str
    conversation: Optional[List[Dict]] = []

@app.post("/verify_token")
async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            "614936797883-64ho69sc6hoefqn0oqkeq84t48q2369c.apps.googleusercontent.com"
        )
        
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid issuer')
            
        return {"valid": True, "user_id": idinfo['sub']}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/chat")
async def chat(
    chat_message: ChatMessage,
    token_data: dict = Depends(verify_token),
    chatgpt: ChatGPT = Depends(get_chatgpt)
):
    # Remove the direct call to verify_token(...)
    if chat_message.conversation:
        chatgpt.conversation_history = [
            {"role": "system", "content": ChatGPT.SYSTEM_PROMPT},
            *chat_message.conversation
        ]
    response = await chatgpt.get_response(chat_message.message)
    return {"response": response}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}