# backend/app/models/response.py

from pydantic import BaseModel
from typing import List

class Citation(BaseModel):
    doc_id: str
    page: int
    paragraph: int

class QAResponse(BaseModel):
    answer: str
    citations: List[Citation]
