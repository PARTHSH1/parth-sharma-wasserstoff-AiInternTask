# backend/app/services/embedding_service.py

import json
import os
from app.core.embedding import get_embedding_model
from app.core.faiss_utils import save_faiss_index

def embed_document_chunks(doc_id: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # path to embedding_service.py
    file_path = os.path.normpath(
        os.path.join(base_dir, '..', '..', 'data', 'extracted_chunks', f"{doc_id}.json")
    )

    print(f"Looking for file at: {file_path}")  # Optional debug line

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk['text'] for chunk in chunks]
    metadatas = [
        {
            "doc_id": doc_id,
            "page": chunk["page"],
            "paragraph": chunk["paragraph"]
        }
        for chunk in chunks
    ]

    embeddings = get_embedding_model()
    save_faiss_index(texts, metadatas, embeddings)
    return {"doc_id": doc_id, "chunks_embedded": len(texts)}