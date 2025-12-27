# Technical Design Document  
## Agentic RAG Assistant — AWS RAG Prescriptive Guidance

### Author
Tyagesh Parmar  
AI Engineer | Data Scientist

---

## 1. Introduction

This document describes the design and implementation of an **Agentic Retrieval-Augmented Generation (RAG) Assistant** built to answer complex questions about **RAG options and architectures on AWS**, strictly grounded in the AWS Prescriptive Guidance document.

The system demonstrates:
- End-to-end RAG pipeline implementation
- Agent-based orchestration with clear role separation
- Grounded, citation-based responses with zero hallucination
- Production-oriented software engineering practices

---

## 2. Problem Statement

Large Language Models (LLMs) are powerful but suffer from:
- Hallucinations
- Lack of access to proprietary documents
- No built-in citation mechanism

The goal is to design a system that can:
- Answer questions using **only a specific document**
- Provide **transparent citations**
- Clearly explain *how* answers are derived

---

## 3. Why Retrieval-Augmented Generation (RAG)

The AWS guide outlines multiple options for querying custom documents:
- Fine-tuning
- In-context learning
- Retrieval-Augmented Generation (RAG)

RAG was selected because:
- It avoids retraining models
- It supports frequently changing documents
- It reduces hallucination risk
- It enables explicit source citation

---

## 4. System Architecture Overview

The system follows an **Agentic Architecture**, where each agent has a single, well-defined responsibility.

### High-Level Flow

User Query  
→ Planner Agent  
→ Retrieval Agent  
→ Synthesis Agent  
→ Generator Agent  
→ Final Grounded Answer

---

## 5. Agent Responsibilities

### 5.1 Planner Agent
- Analyzes the user query
- Identifies query type (comparison, explanation, recommendation)
- Selects relevant document sections for retrieval

### 5.2 Retrieval Agent
- Executes semantic similarity search
- Applies section-based filtering
- Returns ranked passages with metadata and similarity scores
- Falls back to semantic-only retrieval if needed

### 5.3 Synthesis Agent
- Cleans retrieved passages
- Removes table-of-contents noise and fragments
- Merges relevant content
- Builds comparison tables when applicable
- Attaches citations (section name + passage IDs)

### 5.4 Generator Agent
- Uses a Groq-hosted LLM
- Receives only synthesized evidence
- Enforces strict grounding rules
- Explicitly refuses to answer when information is unavailable

---

## 6. RAG Pipeline Design

### Document Processing
- PDF parsed using PyPDF
- Paragraph-level semantic chunking
- Metadata preserved (section, page, passage ID)

### Embedding & Indexing
- SentenceTransformers (`all-MiniLM-L6-v2`)
- ChromaDB persistent vector store
- Supports similarity search and filtering

### Retrieval
- Top-k similarity search
- Section-aware retrieval strategy

### Generation
- Prompt augmented with retrieved evidence
- Deterministic generation (temperature = 0)
- Mandatory citation inclusion

---

## 7. Grounding & Hallucination Prevention

The system enforces grounding through:
- Single-source knowledge base
- Strict system prompt constraints
- Evidence-first synthesis
- Explicit fallback message when information is missing

This ensures high trust and transparency.

---

## 8. Observability & Traceability

The system logs:
- Planner decisions
- Retrieved passages and scores
- Synthesis behavior
- Final grounded answer

This makes agent decisions observable and auditable.

---

## 9. Deployment & Reproducibility

- Front-end built with Streamlit
- Deployed on Streamlit Community Cloud
- Secrets managed via environment variables
- No sensitive data committed to GitHub

---

## 10. Limitations & Future Improvements

### Current Limitations
- Single-document knowledge base
- Rule-based planner logic

### Future Improvements
- Multi-document ingestion
- Advanced query classification
- Reranking with cross-encoders
- User feedback loop

---

## 11. Conclusion

This project demonstrates a robust, transparent, and production-oriented approach to building an **Agentic RAG system**, aligned with AWS best practices and modern AI engineering standards.
