from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_rejects_empty_question():
    response = client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "question": "",
        },
    )

    assert response.status_code == 422


def test_chat_rejects_question_over_1000_characters():
    question = "a" * 1001

    response = client.post(
        "/chat",
        json={
            "session_id": "test1-session",
            "question": question,
        },
    )

    assert response.status_code == 422


def test_chat_rejects_missing_session_id():
    response = client.post(
        "/chat",
        json={
            "question": "What is the asset approval process?",
        },
    )

    assert response.status_code == 422