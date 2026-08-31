from app.conversation.question_resolver import QuestionResolver


class FakeLLM:

    def __init__(self, response):
        self.response = response
        self.called = False

    def generate(self, prompt: str) -> str:
        self.called = True
        return self.response


def test_resolver_returns_original_question_without_history():

    llm = FakeLLM("should not be called")

    resolver = QuestionResolver(llm)

    question = "What is the asset approval process?"

    result = resolver.resolve(
        question=question,
        history="No previous conversation.",
    )

    assert result == question
    assert llm.called is False


def test_resolver_rewrites_follow_up_question():

    llm = FakeLLM(
        "Who approves the IT asset request?"
    )

    resolver = QuestionResolver(llm)

    result = resolver.resolve(
        question="Who approves it?",
        history=(
            "USER: What is the IT asset approval process?\n"
            "ASSISTANT: The process requires Admin approval."
        ),
    )

    assert result == "Who approves the IT asset request?"
    assert llm.called is True