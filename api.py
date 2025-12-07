from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import traceback
import ollama

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

FAISS_PATH = "azure_cloud_computing_and_development_fundamentals_faiss"
OLLAMA_MODEL = "phi3:mini"
TOP_K = 3

vectorstore = None
embeddings = None


def initialize_vectorstore():
    """Load FAISS vectorstore with embeddings"""
    global vectorstore, embeddings

    try:
        logger.info("Loading HuggingFace embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        logger.info(f"Loading FAISS from: {FAISS_PATH}")
        vectorstore = FAISS.load_local(
            folder_path=FAISS_PATH,
            embeddings=embeddings,
            allow_dangerous_deserialization=True,
            index_name="index"
        )

        logger.info("Vectorstore loaded successfully.")
        return True

    except Exception as e:
        logger.error(f"Error loading FAISS store: {e}")
        logger.error(traceback.format_exc())
        return False


with app.app_context():
    initialize_vectorstore()


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "vectorstore_loaded": vectorstore is not None,
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Question is required"}), 400

        docs = vectorstore.similarity_search(question, k=data.get("top_k", TOP_K))
        context = "\n".join([d.page_content for d in docs])

        prompt = f"""
You are a helpful AI assistant.
Answer based ONLY on the context below.
If the answer is not present, say you don’t know.

Context:
{context}

Question: {question}
"""

        logger.info(f"Querying Ollama model {OLLAMA_MODEL}...")

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        answer = response["message"]["content"]

        return jsonify({
            "question": question,
            "answer": answer,
            "context_snippets": [d.page_content[:200] for d in docs],
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/retrieve", methods=["POST"])
def retrieve():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        top_k = data.get("top_k", TOP_K)

        docs = vectorstore.similarity_search(query, k=top_k)

        return jsonify({
            "documents": [
                {"content": d.page_content, "metadata": getattr(d, "metadata", {})}
                for d in docs
            ],
            "count": len(docs)
        })

    except Exception as e:
        logger.error(f"Retrieve error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "RAG API Running"})


if __name__ == "__main__":
    logger.info("🚀 Starting RAG API server...")
    app.run(host="0.0.0.0", port=5000)
