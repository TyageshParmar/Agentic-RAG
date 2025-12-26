import chromadb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
VECTOR_DIR = os.path.join(PROJECT_ROOT, "vectorstore", "chroma_db")

COLLECTION_NAME = "aws_rag_chunks"

client = chromadb.PersistentClient(path=VECTOR_DIR)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

count = collection.count()
print(f"🔎 Collection vector count: {count}")

if count == 0:
    raise RuntimeError("❌ Chroma collection is EMPTY")

print(f"✅ Chroma collection ready: {COLLECTION_NAME}")


def retrieve(query: str, section: str = None, top_k: int = 5):
    results = collection.query(
        query_texts=[query],
        n_results=top_k * 3,
        include=["documents", "metadatas", "distances"]
    )

    retrieved = []
    for i in range(len(results["documents"][0])):
        r = {
            "passage_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "section": results["metadatas"][0][i].get("section", "General"),
            "page": results["metadatas"][0][i].get("page", -1),
            "score": results["distances"][0][i]
        }
        if section and section.lower() not in r["section"].lower():
            continue
        retrieved.append(r)
        if len(retrieved) >= top_k:
            break

    return retrieved