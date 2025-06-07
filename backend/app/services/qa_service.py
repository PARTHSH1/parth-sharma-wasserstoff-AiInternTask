from app.core.embedding import get_embedding_model
from app.core.faiss_utils import query_faiss_index
from app.core.llm import query_llm
def answer_question(question: str, k: int = 5):
    embeddings = get_embedding_model()
    docs = query_faiss_index(question, embeddings, k)

    # Combine all retrieved chunks
    context = "\n\n".join([doc.page_content for doc in docs])

    # Ask the LLM
    answer = query_llm(question, context)

    # Extract citations
    citations = []
    for doc in docs:
        meta = doc.metadata
        citations.append({
            "doc_id": meta.get("doc_id"),
            "page": meta.get("page"),
            "paragraph": meta.get("paragraph")
        })

    return {
        "answer": answer,
        "citations": citations
    }