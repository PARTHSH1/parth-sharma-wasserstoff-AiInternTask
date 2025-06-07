# backend/app/services/document_service.py

import os
import json
from app.core.ocr import extract_text_from_pdf, extract_text_from_image

CHUNK_SAVE_PATH = os.path.join(os.path.dirname(__file__), "../../data/extracted_chunks")
os.makedirs(CHUNK_SAVE_PATH, exist_ok=True)

def process_document(file_path: str):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in ['.pdf']:
        chunks = extract_text_from_pdf(file_path)
    elif ext in ['.png', '.jpg', '.jpeg']:
        chunks = extract_text_from_image(file_path)
    else:
        raise Exception("Unsupported file type")

    # Save chunks
    doc_id = os.path.basename(file_path).split('.')[0]
    with open(os.path.join(CHUNK_SAVE_PATH, f"{doc_id}.json"), 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2)
    return {"doc_id": doc_id, "chunks": len(chunks)}
