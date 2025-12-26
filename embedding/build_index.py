import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
VECTOR_DIR = os.path.join(PROJECT_ROOT, "vectorstore", "chroma_db")

COLLECTION_NAME = "aws_rag_chunks"
os.makedirs(VECTOR_DIR, exist_ok=True)

print("🔢 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=VECTOR_DIR
)

# 🔥 CRITICAL FIX
try:
    client.delete_collection(name=COLLECTION_NAME)
    print("🗑️ Existing collection deleted")
except Exception:
    pass

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

print("📂 Loading chunks...")
with open(os.path.join(PROJECT_ROOT, "output", "chunks.json"), "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"✅ Loaded {len(chunks)} chunks")

documents, metadatas, ids = [], [], []

for i, c in enumerate(chunks):
    documents.append(c["text"])
    metadatas.append({
        "section": c.get("section", "General"),
        "page": c.get("page", -1)
    })
    ids.append(f"auto_{i}")

print("⚙️ Creating embeddings...")
embeddings = model.encode(
    documents,
    batch_size=32,
    show_progress_bar=True
)

collection.add(
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings.tolist(),
    ids=ids
)

print("✅ Vector index created successfully!")
print("🔎 Collection vector count:", collection.count())