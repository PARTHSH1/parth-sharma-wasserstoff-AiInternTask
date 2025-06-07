# backend/app/services/theme_service.py

from app.core.embedding import get_embedding_model
from app.core.faiss_utils import query_faiss_index
from app.core.theme_extraction import extract_themes_from_answers, analyze_chunk

def answer_with_themes(question: str, k: int = 5):
    embeddings = get_embedding_model()
    docs = query_faiss_index(question, embeddings, k)

    doc_answers = []

    for doc in docs:
        meta = doc.metadata
        doc_id = meta.get("doc_id")
        page = meta.get("page", 1)
        para = meta.get("paragraph", 1)
        content = doc.page_content[:1000]  # Truncate if needed

        # Run chunk through mini-LLM summarizer
        summarized = analyze_chunk(doc_id, page, para, content)
        doc_answers.append(summarized)

    # Send short answers to theme extractor
    theme_summary = extract_themes_from_answers(doc_answers)

    return {
        "theme_summary": theme_summary,
        "raw_answers": doc_answers
    }
