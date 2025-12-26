from typing import Dict
from retrieval.retriever import retrieve


class RetrievalAgent:
    def __init__(self, top_k: int = 5):
        self.top_k = top_k

    def retrieve_for_plan(self, plan: Dict) -> Dict:
        query = plan["query"]
        sections = plan["sections_to_search"]

        print("\n🔍 Retriever Agent Execution")
        print(f"Query: {query}")
        print(f"Target sections: {sections}")

        all_results = []

        for section in sections:
            print(f"\n→ Retrieving from section: {section}")

            # 🔥 FIRST TRY: section-aware retrieval
            results = retrieve(
                query=query,
                section=section,
                top_k=self.top_k
            )

            # 🔁 FALLBACK: semantic-only retrieval
            if not results:
                print(f"⚠️ No section-specific hits, retrying without section filter...")
                results = retrieve(
                    query=query,
                    section=None,
                    top_k=self.top_k
                )

            if not results:
                print("❌ Still no results")
                continue

            for r in results:
                r["retrieved_from"] = section
                all_results.append(r)

        if not all_results:
            print("\n❌ Retriever Agent found no relevant passages.")
        else:
            print(f"\n✅ Retrieved {len(all_results)} total passages")

        return {
            "query": query,
            "results": all_results
        }


# -----------------------------
# QUICK TEST
# -----------------------------
if __name__ == "__main__":
    from agents.planner import PlannerAgent

    planner = PlannerAgent()
    retriever_agent = RetrievalAgent(top_k=3)

    query = "Compare fully managed RAG options with custom architectures"

    plan = planner.plan(query)
    output = retriever_agent.retrieve_for_plan(plan)

    print("\n📄 Retrieved Passages Preview:\n")
    for p in output["results"]:
        print(
            f"[{p['passage_id']}] "
            f"(Section: {p['section']}, Score: {p['score']:.4f})"
        )
        print(p["text"][:300])
        print("-" * 80)