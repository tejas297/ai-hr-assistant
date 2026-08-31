from app.database.models import Message


def build_history(messages: list[Message]) -> str:

    if not messages:
        return "No previous conversation."

    lines = []

    for message in messages:
        role = message.role.upper()

        lines.append(
            f"{role}: {message.content}"
        )

    return "\n".join(lines)