from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from chatgpt import ChatGPT
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests
from functools import lru_cache
import time
from collections import defaultdict
from fastapi.responses import JSONResponse

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

# Add rate limiting configuration
RATE_LIMIT_DURATION = 20  # Window Duration
RATE_LIMIT_REQUESTS = 5  # Maximum requests per window

# Store for rate limiting
app.state.rate_limit_store = defaultdict(list)

async def check_rate_limit(request: Request, token_data: dict = Depends(verify_token)):
    user_id = token_data["user_id"]
    now = time.time()
    rate_limit_store = request.app.state.rate_limit_store
    
    # Cleanup old entries completely
    cutoff = now - RATE_LIMIT_DURATION
    for user in list(rate_limit_store.keys()):
        # Remove old timestamps
        rate_limit_store[user] = [t for t in rate_limit_store[user] if t > cutoff]
        # Remove user if no recent requests
        if not rate_limit_store[user]:
            del rate_limit_store[user]
    
    # Check current user's limit
    rate_limit_store[user_id] = [
        req_time for req_time in rate_limit_store[user_id] 
        if now - req_time < RATE_LIMIT_DURATION
    ]
    
    if len(rate_limit_store[user_id]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )
    
    rate_limit_store[user_id].append(now)
    return True

@app.post("/chat")
async def chat(
    chat_message: ChatMessage,
    rate_limit: bool = Depends(check_rate_limit),
    token_data: dict = Depends(verify_token),
    chatgpt: ChatGPT = Depends(get_chatgpt)
):
    rate_limit_store = app.state.rate_limit_store
    user_id = token_data["user_id"]
    requests_remaining = RATE_LIMIT_REQUESTS - len(rate_limit_store[user_id])
    
    response = await chatgpt.get_response(chat_message.message)
    return JSONResponse(
        content={"response": response},
        headers={
            "X-RateLimit-Limit": str(RATE_LIMIT_REQUESTS),
            "X-RateLimit-Remaining": str(requests_remaining),
            "X-RateLimit-Reset": str(int(time.time() + RATE_LIMIT_DURATION))
        }
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}