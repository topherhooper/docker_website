from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from chatgpt import ChatGPT
from google.oauth2 import id_token
from google.auth.transport import requests

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173", 
        "https://topherhooper.com",
        "https://chatbot-frontend-614936797883.us-central1.run.app",  # Frontend Cloud Run URL
        "https://chatbot-backend-614936797883.us-central1.run.app"    # Backend Cloud Run URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChatGPT
chatgpt = ChatGPT()

security = HTTPBearer()

class ChatMessage(BaseModel):
    message: str
    conversation: list[dict] = []  # Optional conversation history

@app.post("/verify_token")
async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        # Specify the CLIENT_ID of your app
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
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    # Verify token before processing chat
    try:
        await verify_token(credentials)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    try:
        # If conversation history is provided, update chatbot's history
        if chat_message.conversation:
            chatgpt.conversation_history = [
                {"role": "system", "content": ChatGPT.SYSTEM_PROMPT},
                *chat_message.conversation
            ]
            
        response = await chatgpt.get_response(chat_message.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}