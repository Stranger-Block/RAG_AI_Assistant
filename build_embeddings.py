import json
import os

from sentence_transformers import SentenceTransformer
import numpy as np

try:
    import faiss
except Exception:
    faiss = None

chunks_file = "D:/RAG_AI_Assistant/azure_cloud_computing_and_development_fundamentals_chunks.json"

if not os.path.exists(chunks_file):
    local_candidate = os.path.join(os.path.dirname(__file__), "azure_cloud_computing_and_development_fundamentals_chunks.json")
    if os.path.exists(local_candidate):
        chunks_file = local_candidate

if not os.path.exists(chunks_file):
    raise FileNotFoundError(f"Chunks JSON file not found at {chunks_file}")

with open(chunks_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c.get("content", "") for c in chunks]
print(f"✅ Loaded {len(texts)} text chunks from {chunks_file}")


print("⏳ Initializing SentenceTransformer (all-MiniLM-L6-v2)")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Initialized SentenceTransformer embeddings (all-MiniLM-L6-v2)")

embs = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
if not isinstance(embs, np.ndarray):
    embs = np.array(embs)

if embs.ndim == 1:
    embs = embs.reshape(1, -1)

print(f"✅ Computed embeddings shape: {embs.shape}")

if faiss is None:
    raise ImportError("faiss not available. Install `faiss-cpu` (or `faiss`) to build the index.")

d = embs.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embs.astype('float32'))
print(f"✅ FAISS index built with {index.ntotal} vectors (dim={d})")

preferred_dir = "D:/RAG_AI_Assistant/azure_cloud_computing_and_development_fundamentals_faiss"
try:
    root = os.path.splitdrive(preferred_dir)[0]
    drive_exists = bool(root) and os.path.exists(root + os.sep)
except Exception:
    drive_exists = False

if drive_exists:
    faiss_dir = preferred_dir
else:
    faiss_dir = os.path.join(os.path.dirname(__file__), "azure_cloud_computing_and_development_fundamentals")

os.makedirs(faiss_dir, exist_ok=True)
index_path = os.path.join(faiss_dir, "index.faiss")
faiss.write_index(index, index_path)

# Save metadata (texts -> ids)
meta = {"texts": texts}
with open(os.path.join(faiss_dir, "metadata.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print(f"✅ FAISS index saved to: {index_path}")
print(f"✅ Metadata saved to: {os.path.join(faiss_dir, 'metadata.json')}")
print("All done! The FAISS vectorstore is ready to be used in your RAG chatbot.")
