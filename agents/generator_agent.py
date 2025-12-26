import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GeneratorAgent:
    """
    Generator Agent (Groq LLM)
    --------------------------
    Uses Groq-hosted LLMs for grounded generation.
    The model is STRICTLY limited to provided context.
    """

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        self.model = model

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)

    def generate(self, query: str, context: str) -> str:
        system_prompt = (
            "You are a grounded RAG assistant.\n"
            "You MUST answer ONLY using the provided context.\n"
            "If the context does not contain sufficient information, reply EXACTLY with:\n"
            "'This information is not available in the provided AWS RAG guide.'\n"
            "Do NOT add external knowledge. Do NOT speculate."
        )

        user_prompt = f"""
QUESTION:
{query}

CONTEXT:
{context}

INSTRUCTIONS:
- Answer clearly and professionally
- Structure the response (headings / bullets) if helpful
- Cite section names when possible
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )

        return response.choices[0].message.content.strip()