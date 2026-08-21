from dotenv import load_dotenv

from app.llm.groq_client import GroqClient


load_dotenv()


def main():
    llm = GroqClient()

    prompt = """
You are an AI HR Assistant.

Answer the following question briefly.

Question:
What is an HR policy?

Answer:
"""

    answer = llm.generate(prompt)

    print("===== ANSWER =====")
    print(answer)
    print("==================")


if __name__ == "__main__":
    main()