class PlannerAgent:
    """
    Planner Agent
    -------------
    Converts a user query into a structured retrieval plan.
    """

    def plan(self, query: str) -> dict:
        return {
            "query": query,
            "sections_to_search": [
                "Fully managed RAG options",
                "Custom RAG architectures"
            ]
        }