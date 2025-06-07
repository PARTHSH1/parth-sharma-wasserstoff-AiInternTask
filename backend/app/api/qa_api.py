from fastapi import APIRouter
from app.models.query import QueryRequest
from app.models.response import QAResponse
from app.services.qa_service import answer_question

router = APIRouter()

@router.post("/query", response_model=QAResponse)
async def query_documents(payload: QueryRequest):
    result = answer_question(payload.question)
    return result
