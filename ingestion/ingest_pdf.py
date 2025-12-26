import json
import os
from tqdm import tqdm
from pypdf import PdfReader

PDF_PATH = "data/retrieval-augmented-generation-options.pdf"
OUTPUT_PATH = "output/chunks.json"

os.makedirs("output", exist_ok=True)


def detect_section(text: str) -> str:
    t = text.lower()

    if "fully managed" in t or "knowledge bases for amazon bedrock" in t or "amazon q" in t:
        return "Fully managed RAG options"

    if "custom retrieval augmented generation" in t or "custom rag" in t:
        return "Custom RAG architectures"

    if any(k in t for k in [
        "amazon kendra", "opensearch", "aurora", "neptune",
        "memorydb", "documentdb", "pinecone", "mongodb", "weaviate"
    ]):
        return "Retrievers"

    if any(k in t for k in [
        "amazon bedrock", "sagemaker", "jumpstart", "foundation model", "llm"
    ]):
        return "Generators"

    return "General"


print("📄 Loading PDF documents...")
reader = PdfReader(PDF_PATH)

chunks = []
para_id = 0

for page_num, page in enumerate(reader.pages):
    text = page.extract_text()
    if not text:
        continue

    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 40]

    for para in paragraphs:
        chunk = {
            "passage_id": f"para_{para_id:04d}",
            "text": para,
            "section": detect_section(para),
            "page": page_num + 1
        }
        chunks.append(chunk)
        para_id += 1

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print(f"💾 Saved {len(chunks)} chunks to {OUTPUT_PATH}")