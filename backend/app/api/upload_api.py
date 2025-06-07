from fastapi import APIRouter, File, UploadFile
import shutil
import os

from app.config import UPLOAD_DIR
from app.services.document_service import process_document
from app.services.embedding_service import embed_document_chunks

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Step 1: Save file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Step 2: Process (OCR + extract)
    doc_info = process_document(file_location)
    doc_id = doc_info["doc_id"]
    chunks = doc_info["chunks"]

    # Step 3: Embed chunks and store in FAISS
    embedding_info = embed_document_chunks(doc_id)

    return {
        "message": "File uploaded, processed, and embedded",
        "doc_id": doc_id,
        "chunks_extracted": chunks,
        "chunks_embedded": embedding_info["chunks_embedded"]
    }
