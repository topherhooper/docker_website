# llm-chat/backend/app/api/models.py
from pydantic import BaseModel
from typing import List

class Document(BaseModel):
    content: str
    metadata: dict

class Query(BaseModel):
    question: str
    doc_ids: List[str]