# backend/app/main.py

from fastapi import FastAPI
from app.api import upload_api, qa_api  # ✅ Import both upload and query APIs
from app.api import upload_api, qa_api, theme_api
app = FastAPI()

# Include routers
app.include_router(upload_api.router, prefix="/api")
app.include_router(qa_api.router, prefix="/api")  # ✅ Add this line

@app.get("/")
def read_root():
    return {"message": "Wasserstoff Chatbot Backend"}

app.include_router(theme_api.router, prefix="/api")
