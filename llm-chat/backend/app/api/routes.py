from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from ..core.config import settings
from ..utils.cache import redis_client
from .models import Document, Query

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.allowed_origins,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# llm-chat/backend/app/api/routes.py
@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.post("/documents")
@limiter.limit(settings.rate_limit_documents)
async def upload_document(request: Request, document: Document):
    try:
        # Add document storage logic here
        return {"status": "success", "message": "Document uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
@limiter.limit(settings.rate_limit_queries)
async def query_documents(request: Request, query: Query):
    cache_key = f"query:{query.question}:{','.join(query.doc_ids)}"
    cached_response = redis_client.get(cache_key)
    
    if cached_response:
        return {"response": cached_response.decode()}
    
    try:
        # Add LLM query logic here
        response = "Sample response"
        redis_client.setex(cache_key, 3600, response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}