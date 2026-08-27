from app.conversation.service import ConversationService
from app.database.models import Conversation, Message


def test_get_or_create_conversation_creates_new_conversation():
    service = ConversationService()

    class FakeDB:
        def __init__(self):
            self.added = []
            self.committed = False

        def scalar(self, statement):
            return None

        def add(self, obj):
            self.added.append(obj)

        def commit(self):
            self.committed = True

        def refresh(self, obj):
            obj.id = 1

    db = FakeDB()

    conversation = service.get_or_create_conversation(
        db=db,
        session_id="test-session",
    )

    assert isinstance(conversation, Conversation)
    assert conversation.session_id == "test-session"
    assert conversation.id == 1
    assert db.committed is True


def test_add_message():
    service = ConversationService()

    class FakeDB:
        def __init__(self):
            self.added = []
            self.committed = False

        def add(self, obj):
            self.added.append(obj)

        def commit(self):
            self.committed = True

        def refresh(self, obj):
            obj.id = 1

    db = FakeDB()

    message = service.add_message(
        db=db,
        conversation_id=1,
        role="user",
        content="What is the asset approval process?",
    )

    assert isinstance(message, Message)
    assert message.conversation_id == 1
    assert message.role == "user"
    assert message.content == "What is the asset approval process?"
    assert message.id == 1
    assert db.committed is True