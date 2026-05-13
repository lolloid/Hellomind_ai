import logging
from dataclasses import dataclass

from django.conf import settings
import httpx
from openai import APIConnectionError, APIStatusError, AuthenticationError, RateLimitError
from openai import OpenAI


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AIReplyResult:
    reply: str = ""
    provider: str = "groq"
    status: str = "not_requested"
    fallback_reason: str = ""
    finish_reason: str = ""


def get_client() -> OpenAI:
    http_client = httpx.Client(
        timeout=settings.GROQ_TIMEOUT_SECONDS,
        trust_env=settings.GROQ_TRUST_ENV,
    )
    return OpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url=settings.GROQ_BASE_URL,
        http_client=http_client,
        timeout=settings.GROQ_TIMEOUT_SECONDS,
    )


def get_provider_config() -> dict:
    return {
        "provider": "groq",
        "base_url": settings.GROQ_BASE_URL,
        "model": settings.GROQ_MODEL,
        "has_api_key": bool(settings.GROQ_API_KEY),
        "trust_env_proxy": settings.GROQ_TRUST_ENV,
        "timeout_seconds": settings.GROQ_TIMEOUT_SECONDS,
    }


def check_groq_connection() -> dict:
    result = get_provider_config()
    if not settings.GROQ_API_KEY:
        return {
            **result,
            "ok": False,
            "status": "missing_api_key",
            "message": "GROQ_API_KEY is not configured.",
        }

    try:
        response = get_client().chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Reply with exactly: ok"},
                {"role": "user", "content": "health check"},
            ],
            temperature=0,
            max_tokens=8,
        )
        reply = (response.choices[0].message.content or "").strip()
        return {
            **result,
            "ok": bool(reply),
            "status": "ok" if reply else "empty_response",
            "message": reply or "Groq returned an empty response.",
        }
    except AuthenticationError as exc:
        logger.warning("Groq authentication failed: %s", exc)
        return {
            **result,
            "ok": False,
            "status": "invalid_api_key",
            "message": "Groq rejected GROQ_API_KEY. Create a new key and update .env.",
        }
    except APIConnectionError as exc:
        logger.warning("Groq connection failed: %s", exc)
        return {
            **result,
            "ok": False,
            "status": "connection_error",
            "message": "Could not connect to Groq. Check network/proxy settings.",
        }
    except APIStatusError as exc:
        logger.warning("Groq API status error: %s", exc)
        return {
            **result,
            "ok": False,
            "status": f"api_status_{exc.status_code}",
            "message": str(exc),
        }
    except Exception as exc:
        logger.exception("Groq health check failed")
        return {
            **result,
            "ok": False,
            "status": "unknown_error",
            "message": str(exc),
        }


def generate_chat_reply_result(messages: list[dict], language: str = "id") -> AIReplyResult:
    if not settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY is missing")
        return AIReplyResult(status="missing_api_key", fallback_reason="missing_api_key")

    try:
        response = get_client().chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            temperature=0.85,
            top_p=0.95,
            max_tokens=200,
        )
        reply = (response.choices[0].message.content or "").strip()
        finish_reason = getattr(response.choices[0], "finish_reason", "") or ""
    except AuthenticationError:
        logger.error("Groq authentication failed. Update GROQ_API_KEY in .env.")
        return AIReplyResult(status="invalid_api_key", fallback_reason="invalid_api_key")
    except RateLimitError as exc:
        logger.warning("Groq rate limit reached. Falling back to local supportive reply. status=%s", exc.status_code)
        return AIReplyResult(status="rate_limited", fallback_reason="rate_limited")
    except APIConnectionError as exc:
        logger.warning("Groq connection failed. Falling back to local supportive reply: %s", exc)
        return AIReplyResult(status="connection_error", fallback_reason="connection_error")
    except APIStatusError as exc:
        logger.warning(
            "Groq API returned a non-success status. Falling back to local supportive reply. status=%s",
            exc.status_code,
        )
        return AIReplyResult(status=f"api_status_{exc.status_code}", fallback_reason="api_status_error")
    except Exception:
        logger.exception("Groq API request failed unexpectedly")
        return AIReplyResult(status="unknown_error", fallback_reason="unknown_error")

    if reply:
        return AIReplyResult(reply=reply, status="ok", finish_reason=finish_reason)

    logger.warning("Groq returned an empty chat completion.")
    return AIReplyResult(status="empty_response", fallback_reason="empty_response", finish_reason=finish_reason)


def generate_chat_reply(messages: list[dict], language: str = "id") -> str:
    return generate_chat_reply_result(messages, language).reply
