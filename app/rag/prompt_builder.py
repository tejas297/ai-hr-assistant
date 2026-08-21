SYSTEM_PROMPT = """You are an AI HR Assistant.

Your job is to answer employee questions using only the provided HR policy context.

Rules:
1. Answer only using information present in the provided context.
2. Do not use your own knowledge to fill missing information.
3. If the answer is not present in the context, clearly say that the information could not be found in the available HR policies.
4. Do not invent policies, numbers, dates, benefits, approvals, or procedures.
5. When possible, provide the source document and page number.
"""


def build_prompt(context: str, question: str) -> str:
    if not question.strip():
        raise ValueError("Question cannot be empty")

    if not context.strip():
        raise ValueError("Context cannot be empty")

    return f"""{SYSTEM_PROMPT}

HR POLICY CONTEXT:
------------------
{context}
------------------

EMPLOYEE QUESTION:
{question}

Answer the employee's question using only the HR policy context above.
"""