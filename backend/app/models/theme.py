# backend/app/models/theme.py

from pydantic import BaseModel
from typing import List

class ThemeResponse(BaseModel):
    theme_summary: str
    raw_answers: List[str]
