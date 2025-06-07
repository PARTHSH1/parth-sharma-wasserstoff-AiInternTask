from fastapi import APIRouter
from app.models.query import QueryRequest
from app.models.theme import ThemeResponse
from app.services.theme_service import answer_with_themes

router = APIRouter()

@router.post("/themes", response_model=ThemeResponse)
async def extract_themes_from_query(payload: QueryRequest):
    result = answer_with_themes(payload.question)
    return result
