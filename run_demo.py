from agents.planner import PlannerAgent
from agents.retriever_agent import RetrievalAgent
from agents.synthesis_agent import SynthesisAgent
from agents.generator_agent import GeneratorAgent


query = "Compare fully managed RAG options with custom architectures"

planner = PlannerAgent()
retriever = RetrievalAgent(top_k=5)
synthesizer = SynthesisAgent()
generator = GeneratorAgent()

plan = planner.plan(query)
retrieval_output = retriever.retrieve_for_plan(plan)

# Step 1: evidence synthesis (no LLM)
evidence_text = synthesizer.synthesize(
    query=retrieval_output["query"],
    retrieved_passages=retrieval_output["results"]
)


# Step 2: LLM-based generation (grounded)
final_answer = generator.generate(
    query=query,
    context=evidence_text
)

print("\n" + "=" * 80)
print(final_answer)
print("=" * 80)