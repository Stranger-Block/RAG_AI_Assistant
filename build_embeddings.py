import json
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

CHUNKS_FILE = "azure_cloud_computing_and_development_fundamentals_chunks.json"
OUTPUT_DIR = "azure_cloud_computing_and_development_fundamentals_faiss"

def load_chunks():
    """Load chunks JSON"""
    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(f"Chunks file not found: {CHUNKS_FILE}")

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["content"] for c in chunks if c.get("content")]
    print(f"Loaded {len(texts)} chunks")
    return texts

def save_vectorstore(texts):
    """Create and save FAISS vectorstore"""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    vectorstore.save_local(OUTPUT_DIR)

    print(f"FAISS index saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    texts = load_chunks()
    save_vectorstore(texts)
    print("✅ Finished building FAISS vectorstore.")
