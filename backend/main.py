from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatgpt import ChatGPT

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://127.0.0.1:5173",
        # "http://localhost:5173", 
        # "https://topherhooper.com",
        # "https://chatbot-frontend-614936797883.us-central1.run.app",  # Frontend Cloud Run URL
        # "https://chatbot-backend-614936797883.us-central1.run.app"    # Backend Cloud Run URL
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChatGPT
chatgpt = ChatGPT()

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        response = await chatgpt.get_response(chat_message.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}