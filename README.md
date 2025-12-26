# 🧠 Agentic RAG Assistant — AWS RAG Prescriptive Guidance

🔗 **Live Demo (Streamlit App):**  
👉 https://agentic-rag-aws.streamlit.app/

🔗 **GitHub Repository:**  
👉 https://github.com/TyageshParmar/Agentic-RAG.git

---

## 📌 Project Overview

This project implements an **Agentic Retrieval-Augmented Generation (RAG) assistant** that answers complex questions about **RAG options and architectures on AWS**, **strictly grounded** in the official AWS Prescriptive Guidance document:

> **“Retrieval Augmented Generation options and architectures on AWS”**

The system demonstrates:
- End-to-end **RAG pipeline implementation**
- **Agentic AI architecture** with clear role separation
- **Grounded, citation-based answers** with zero hallucination
- Production-oriented **software engineering practices**

This project was built as part of an **Agentic RAG assignment** and is intended for **technical evaluation by recruiters and reviewers**.

---

## 🚀 Live Demo (Web Interface)

The system is deployed using **Streamlit** for easy online evaluation.

🔗 **Demo URL:**  
👉 https://agentic-rag-aws.streamlit.app/

### Demo Capabilities
- Ask natural-language questions about RAG on AWS
- Observe **agent reasoning** (Planner → Retriever → Synthesizer → Generator)
- View retrieved evidence and citations
- Verify that answers are derived **only from the AWS document**

---

## 🧩 System Architecture (Agentic Design)

The assistant follows a **multi-agent orchestration pattern**, where each agent has a **distinct responsibility**:

### 🧠 Planner Agent
- Analyzes the user query
- Identifies query type (comparison, analysis, recommendation)
- Selects relevant document sections for retrieval

### 🔍 Retrieval Agent
- Performs semantic similarity search over a vector database
- Supports **section-based filtering**
- Returns ranked passages with metadata and confidence scores

### 🧩 Synthesis Agent
- Combines retrieved passages into structured evidence
- Removes noise (TOC fragments, short text)
- Builds comparison tables when applicable
- Attaches explicit citations (section + passage IDs)

### 🤖 Generator Agent
- Uses a Groq-hosted LLM for final answer generation
- **Strictly limited to synthesized context**
- Explicitly refuses to answer if information is missing

---

## 📄 Knowledge Source (Single Source of Truth)

- **AWS Prescriptive Guidance PDF**
- Treated as the **only ground-truth knowledge base**
- No external data or model knowledge is used

This guarantees:
- No hallucinations
- Transparent citations
- Honest “information not available” responses

---

## 🛠️ RAG Pipeline Overview

1. **Document Ingestion**
   - PDF loading and text extraction
   - Paragraph-level semantic chunking
   - Metadata preservation (section, page, passage ID)

2. **Embedding & Indexing**
   - SentenceTransformers (`all-MiniLM-L6-v2`)
   - Vector storage using **ChromaDB**
   - Supports similarity search and filtering

3. **Retrieval**
   - Top-k semantic similarity search
   - Section-aware retrieval with fallback

4. **Generation**
   - Prompt augmented with retrieved context
   - Grounded answer generation with citations

---

## 🧪 Example Queries the Assistant Can Handle

The system is designed to robustly answer queries such as:

1. *What are the main generative AI options for querying custom documents, and where does RAG fit among them?*
2. *Compare fully managed RAG options on AWS with custom RAG architectures. When would you choose each?*
3. *List the retriever options described in the guide and their key characteristics.*
4. *How does the guide compare RAG vs. fine-tuning? What are the trade-offs?*
5. *Which RAG option is suitable for enterprise search over PDFs and internal wikis, and why?*
6. *What is the role of a generator in RAG, and which AWS services can act as generators?*
7. *What are the trade-offs between managed knowledge bases and custom RAG architectures?*

---

## 🖥️ Running the Project Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/TyageshParmar/Agentic-RAG.git
cd Agentic-RAG
```
````markdown
# Agentic RAG AWS Guide - Setup & Deployment

## 1️⃣ Overview

This project demonstrates how to design, implement, and deploy an **Agentic RAG system** that is:

- Transparent  
- Grounded  
- Production-oriented  

using the AWS RAG Prescriptive Guidance PDF as the sole knowledge source.  
The system includes a **multi-agent pipeline** (Planner, Retriever, Synthesis, Generator) and a web interface for querying.

---

## 2️⃣ Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
````

---

## 3️⃣ Set Environment Variables

Create a `.env` file (do **not** commit to GitHub):

```env
GROQ_API_KEY=your_groq_api_key_here
```

> A `.env.example` file is provided for reference.

---

## 4️⃣ Document Ingestion & Indexing

Run the ingestion pipeline:

```bash
python ingestion/ingest_pdf.py
python ingestion/build_index.py
```

This will:

* Parse the AWS PDF
* Generate chunks
* Build a persistent **Chroma vector index**

---

## 5️⃣ Run the Web Interface

```bash
streamlit run app.py
```

The app will open in your browser and provide:

* Query input
* Agent reasoning traces
* Retrieved evidence
* Final grounded answers

---

## 6️⃣ Deployment (Cloud-Based)

* Front-end deployed using **Streamlit Community Cloud**
* Secrets managed via **Streamlit Secrets** (no `.env` files committed)
* Live app: [Agentic RAG Demo](https://agentic-rag-aws.streamlit.app/)

---

## 7️⃣ Security & Best Practices

* `.env` is **never committed**
* `.env.example` included for reproducibility
* API keys are managed via environment variables
* No hard-coded secrets

---

## 8️⃣ Assignment Deliverables (Compliance)

✔ Complete Agentic RAG pipeline
✔ Multi-agent architecture
✔ Grounded, citation-based answers
✔ Reproducible codebase
✔ Public GitHub repository
✔ Online Streamlit demo

---

## 9️⃣ Key Takeaways

This project demonstrates how to:

* Design an **agentic multi-agent RAG system**
* Implement a **grounded, citation-based pipeline**
* Deploy the system **locally and in the cloud**
* Maintain **security and reproducibility** for AI applications

---

## 10️⃣ Author

**Tyagesh Parmar**
AI Engineer | Data Scientist
GitHub: [https://github.com/TyageshParmar](https://github.com/TyageshParmar)

```
