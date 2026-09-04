from unittest.mock import Mock, patch

from app.rag.rag_service import RAGService, split_reasoning


class FakeLLM:

    def __init__(self):
        self.called = False

    def generate(self, prompt: str) -> str:
        self.called = True
        return "This is a test answer."


def test_split_reasoning_keeps_reasoning_out_of_answer():
    answer, reasoning = split_reasoning(
        "<think>Use the policy context.</think>\nThe policy answer."
    )

    assert answer == "The policy answer."
    assert reasoning == "Use the policy context."


def test_split_reasoning_strips_thinking_prefix_without_tags():
    answer, reasoning = split_reasoning(
        "Here's a thinking process:\n"
        "1. Check the reward policy.\n"
        "2. Summarize the award rules.\n\n"
        "The policy answer."
    )

    assert answer == "The policy answer."
    assert reasoning == "1. Check the reward policy.\n2. Summarize the award rules."


def test_rag_returns_answer_and_sources():

    fake_result = Mock()

    fake_result.chunk.document_name = "asset_approval_policy.pdf"
    fake_result.chunk.page_number = 3
    fake_result.chunk.content = (
        "The Admin department must approve the request and budget."
    )

    rag = RAGService(
        llm=FakeLLM(),
    )

    fake_db = Mock()

    with patch(
        "app.rag.rag_service.search_similar_chunks",
        return_value=[fake_result],
    ):

        response = rag.answer(
            db=fake_db,
            question="Who approves IT assets?",
        )

    assert response.answer == "This is a test answer."

    assert len(response.sources) == 1

    assert response.sources[0].document_name == (
        "asset_approval_policy.pdf"
    )

    assert response.sources[0].page_number == 3

def test_rag_does_not_call_llm_when_no_chunks_found():

    llm = FakeLLM()

    rag = RAGService(
        llm=llm,
    )

    fake_db = Mock()

    with patch(
        "app.rag.rag_service.search_similar_chunks",
        return_value=[],
    ):

        response = rag.answer(
            db=fake_db,
            question="What is the maternity leave policy?",
        )

    assert response.sources == []

    assert response.answer == (
        "I could not find this information "
        "in the available HR policies."
    )

    assert llm.called is False