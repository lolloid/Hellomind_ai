from celery import shared_task

from .services import generate_chat_reply


@shared_task(name="ai_services.generate_chat_reply")
def generate_chat_reply_task(messages: list[dict], language: str = "id") -> str:
    return generate_chat_reply(messages, language)
