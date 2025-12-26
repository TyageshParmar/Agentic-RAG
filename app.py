import streamlit as st
import os
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Import agents (your existing code)
# -----------------------------
from agents.planner import PlannerAgent
from agents.retriever_agent import RetrievalAgent
from agents.synthesis_agent import SynthesisAgent
from agents.generator_agent import GeneratorAgent


# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Agentic RAG Assistant – AWS RAG Guide",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# Title & Description
# -----------------------------
st.title("🧠 Agentic RAG Assistant")
st.subheader("Grounded Question Answering over AWS RAG Prescriptive Guidance")

st.markdown(
    """
This assistant answers **complex questions about RAG options and architectures on AWS**,  
**strictly grounded** in the official AWS Prescriptive Guidance document.

**Key features:**
- Multi-agent architecture (Planner → Retriever → Synthesizer → Generator)
- Retrieval-Augmented Generation (RAG)
- Zero hallucination policy
- Explicit citations from the source document
"""
)

# -----------------------------
# Sidebar – System Info
# -----------------------------
with st.sidebar:
    st.header("⚙️ System Information")

    api_key_present = bool(os.getenv("GROQ_API_KEY"))
    st.write("**GROQ API Key:**", "✅ Loaded" if api_key_present else "❌ Not Found")

    st.markdown("---")
    st.markdown("### 📄 Knowledge Source")
    st.write("AWS Prescriptive Guidance:")
    st.write("Retrieval Augmented Generation options and architectures on AWS")

    st.markdown("---")
    st.markdown("### 🧪 Example Queries")
    st.markdown(
        """
- Compare fully managed RAG options with custom architectures  
- What are the retriever options described in the guide?  
- How does RAG compare with fine-tuning?  
- What is the role of a generator in RAG?  
- Which RAG option is best for enterprise search?
"""
    )

# -----------------------------
# Initialize Agents (cached)
# -----------------------------
@st.cache_resource
def load_agents():
    planner = PlannerAgent()
    retriever = RetrievalAgent(top_k=5)
    synthesizer = SynthesisAgent()
    generator = GeneratorAgent()
    return planner, retriever, synthesizer, generator


planner, retriever, synthesizer, generator = load_agents()

# -----------------------------
# User Query Input
# -----------------------------
st.markdown("## 🔍 Ask a Question")

query = st.text_area(
    "Enter your question about RAG options and architectures:",
    height=100,
    placeholder="e.g. Compare fully managed RAG options on AWS with custom RAG architectures"
)

run_button = st.button("🚀 Run Query")

# -----------------------------
# Main Execution
# -----------------------------
if run_button and query.strip():

    st.markdown("---")

    # -----------------------------
    # Planner Agent
    # -----------------------------
    st.markdown("## 🧠 Planner Agent")

    plan = planner.plan(query)

    st.write("**Query Type:** Comparison / Analysis (rule-based)")
    st.write("**Sections Selected for Retrieval:**")
    for sec in plan.get("sections_to_search", []):
        st.write(f"- {sec}")

    # -----------------------------
    # Retrieval Agent
    # -----------------------------
    st.markdown("## 🔍 Retrieval Agent")

    retrieval_output = retriever.retrieve_for_plan(plan)
    retrieved_passages = retrieval_output.get("results", [])

    if not retrieved_passages:
        st.error("❌ No relevant passages retrieved.")
    else:
        st.success(f"✅ Retrieved {len(retrieved_passages)} passages")

        with st.expander("📄 View Retrieved Evidence"):
            for p in retrieved_passages:
                st.markdown(
                    f"""
**Passage ID:** {p['passage_id']}  
**Section:** {p['section']}  
**Score:** {p['score']:.4f}  

{p['text']}
---
"""
                )

    # -----------------------------
    # Synthesis Agent (No LLM)
    # -----------------------------
    st.markdown("## 🧩 Synthesis Agent")

    evidence_text = synthesizer.synthesize(
        query=retrieval_output["query"],
        retrieved_passages=retrieved_passages
    )

    st.write("**Evidence synthesized from retrieved passages.**")
    with st.expander("🧾 View Synthesized Evidence"):
        st.markdown(evidence_text)

    # -----------------------------
    # Generator Agent (LLM – Grounded)
    # -----------------------------
    st.markdown("## 🤖 Generator Agent (Grounded Answer)")

    final_answer = generator.generate(
        query=query,
        context=evidence_text
    )

    st.success("✅ Final Answer Generated (Grounded & Cited)")
    st.markdown(final_answer)

    st.markdown("---")
    st.caption(
        "⚠️ This system answers **only using the provided AWS RAG guide**. "
        "If information is missing, it explicitly states so."
    )

elif run_button:
    st.warning("Please enter a question before running.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption(
    "Agentic RAG Assistant | Built for Assignment Evaluation & Technical Review"
)
