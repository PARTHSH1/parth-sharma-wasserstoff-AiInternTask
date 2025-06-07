from langchain_community.vectorstores import FAISS
import os
INDEX_DIR = "data/faiss_index"

def save_faiss_index(texts, metadatas, embeddings, save_path=INDEX_DIR):
    os.makedirs(save_path, exist_ok=True) 

    index_file = os.path.join(save_path, "index.faiss")
    if os.path.exists(index_file):
        db_existing = FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
        db_new = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)
        db_existing.merge_from(db_new)
        db_existing.save_local(save_path)
    else:
        db = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)
        db.save_local(save_path)

def load_faiss_index(embeddings, load_path=INDEX_DIR):
    index_file = os.path.normpath(os.path.join(load_path, "index.faiss"))

    if not os.path.exists(index_file):
        raise FileNotFoundError(
            f"FAISS index not found at {index_file}. You must upload at least one document first."
        )
    load_path = os.path.normpath(load_path)
    return FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)


def query_faiss_index(question, embeddings, k=3):
    db = load_faiss_index(embeddings)
    docs = db.similarity_search(question, k=k)
    return docs
