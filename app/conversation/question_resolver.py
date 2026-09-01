import re

from app.llm.client import LLMClient


class QuestionResolver:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def resolve(
        self,
        question: str,
        history: str,
    ) -> str:

        if history == "No previous conversation.":
            return question

        prompt = f"""
You are a question rewriting component for an HR policy RAG system.

Your job is to rewrite the user's latest question into a
self-contained search query.

Use the conversation history only to resolve references such as:
- it
- they
- them
- this
- that
- the process
- the policy
- the department

Do not answer the question.

Do not add facts that are not present in the conversation.

Return ONLY the rewritten question.

Conversation history:
{history}

Latest user question:
{question}

Rewritten question:
""".strip()

        response = self.llm.generate(prompt).strip()

        # Extract content after thinking blocks if present
        resolved = re.sub(
            r"<(?:think|thinking)>.*?</(?:think|thinking)>\s*",
            "",
            response,
            flags=re.IGNORECASE | re.DOTALL,
        ).strip()

        if not resolved:
            return question

        return resolved