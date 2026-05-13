import logging

from django.conf import settings
from django.db import transaction

from apps.ai_services.services import generate_chat_reply_result
from apps.emotion.services import detect_text_emotion
from apps.mood.models import MoodEntry
from apps.persona.services import build_persona_prompt, greeting_reply, infer_persona_style, is_simple_greeting
from apps.safety.services import (
    crisis_message,
    is_off_topic,
    is_policy_violation,
    policy_violation_message,
    risk_level,
)

from .models import Chat, Message


logger = logging.getLogger(__name__)

NEXT_RESPONSE_FOCUS_ID = (
    "Catatan respons berikutnya: utamakan pesan terbaru user dan tanggapi detail konkretnya. "
    "Kalau ini sapaan, balas ringan. Kalau ceritanya lucu atau malu-maluin, ikut bereaksi natural. "
    "Kalau user bertanya atau meminta bantuan teknis/tugas, jawab langsung dengan jelas dan profesional tanpa memaksa mode curhat. "
    "Kalau emosinya berat, beri validasi dan dukungan ringan. Jaga alurnya tetap seperti obrolan biasa."
)

NEXT_RESPONSE_FOCUS_EN = (
    "Next response note: prioritize the user's latest message and react to its concrete details. "
    "If it is a greeting, keep it light. If it is funny or embarrassing, react naturally. "
    "If the user asks a question or requests help, answer directly and professionally without forcing emotional support. "
    "If it is emotionally heavy, validate and offer light support. Keep the flow conversational."
)

OFF_TOPIC_CONTEXT_ID = (
    "Konteks: pesan user tampaknya berupa pertanyaan, tugas, atau percakapan umum. "
    "Jawablah dengan ringkas, jelas, dan profesional layaknya asisten. "
    "Tidak perlu memberikan frasa dukungan emosional untuk pesan jenis ini."
)

OFF_TOPIC_CONTEXT_EN = (
    "Context: the user's message appears to be a question, a task, or a general conversation. "
    "Answer concisely, clearly, and professionally as an assistant. "
    "Do not provide emotional support phrases for this type of message."
)


def truncate_title(text: str) -> str:
    text = text.strip()
    return text[:32] + ("..." if len(text) > 32 else "")


def get_or_create_chat(user, chat_id: int | None, first_message: str) -> Chat:
    if chat_id:
        chat = Chat.objects.filter(id=chat_id, user=user).first()
        if chat:
            return chat
    return Chat.objects.create(user=user, title=truncate_title(first_message) or "Obrolan Baru")


def build_messages(
    chat: Chat,
    system_prompt: str,
    current_message: str,
    language: str = "id",
    off_topic: bool = False,
) -> list[dict]:
    messages = [{"role": "system", "content": system_prompt}]
    previous = list(chat.messages.order_by("-created_at")[: settings.AI_MAX_HISTORY_MESSAGES + 1])
    previous.reverse()

    for item in previous[:-1]:
        role = "user" if item.role == Message.ROLE_USER else "assistant"
        messages.append({"role": role, "content": item.text})

    if off_topic:
        off_topic_prompt = OFF_TOPIC_CONTEXT_EN if language == "en" else OFF_TOPIC_CONTEXT_ID
        messages.append({"role": "system", "content": off_topic_prompt})

    focus_prompt = NEXT_RESPONSE_FOCUS_EN if language == "en" else NEXT_RESPONSE_FOCUS_ID
    messages.append({"role": "system", "content": focus_prompt})
    messages.append({"role": "user", "content": current_message})
    return messages


def has_prior_emotional_context(chat: Chat | None) -> bool:
    if not chat:
        return False
    return chat.messages.filter(role=Message.ROLE_USER).exclude(text_emotion__in=["", "neutral"]).exists()


def recent_user_texts(chat: Chat | None, limit: int = 3) -> list[str]:
    if not chat:
        return []
    messages = chat.messages.filter(role=Message.ROLE_USER).order_by("-created_at")[:limit]
    return [message.text.lower() for message in messages]


def contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def is_casual_embarrassment(text: str) -> bool:
    terms = [
        "salah masuk kelas",
        "salah kelas",
        "salah ruangan",
        "salah room",
        "malu banget",
        "malu sumpah",
        "awkward",
    ]
    return contains_any(text, terms) or ("wkwk" in text and "malu" in text)


def is_casual_mishap(text: str) -> bool:
    mishap_terms = [
        "jatuh",
        "kepleset",
        "kesandung",
        "nabrak",
        "salah kirim",
        "salah ngomong",
        "salah sebut",
        "lupa bawa",
        "telat masuk",
    ]
    casual_markers = ["wkwk", "haha", "😭", "😂", "malu", "sumpah", "anjir", "anjay"]
    return contains_any(text, mishap_terms) and contains_any(text, casual_markers)


def is_sleep_followup(text: str) -> bool:
    terms = [
        "susah tidur",
        "ga bisa tidur",
        "gak bisa tidur",
        "nggak bisa tidur",
        "ngga bisa tidur",
        "insomnia",
        "tidur juga",
    ]
    return contains_any(text, terms)


def recent_mentions_exhaustion(recent_texts: list[str]) -> bool:
    terms = ["capek", "cape", "lelah", "berat", "banyak pikiran", "kepikiran", "overthinking"]
    return any(contains_any(text, terms) for text in recent_texts)


def is_exhaustion_message(text: str) -> bool:
    return contains_any(text, ["capek", "cape", "lelah", "letih", "burnout", "hari ini berat"])


def is_overthinking_message(text: str) -> bool:
    return contains_any(text, ["overthinking", "kepikiran terus", "mikir terus", "pikiran muter", "banyak pikiran"])


def is_life_confusion_message(text: str) -> bool:
    return contains_any(text, ["bingung sama hidup", "bingung hidup", "arah hidup", "hidupku", "masa depanku"])


def is_failure_fear_message(text: str) -> bool:
    return contains_any(text, ["takut gagal", "gagal terus", "takut nggak berhasil", "takut ga berhasil", "takut gak berhasil"])


def is_lonely_message(text: str) -> bool:
    return contains_any(text, ["sendirian", "kesepian", "sepi", "nggak punya tempat cerita", "gak punya tempat cerita"])


def summarize_ai_messages(messages: list[dict]) -> list[dict]:
    summary = []
    for message in messages:
        content = message.get("content", "")
        summary.append(
            {
                "role": message.get("role", ""),
                "chars": len(content),
                "preview": content[:90].replace("\n", " "),
            }
        )
    return summary


def log_generation_debug(
    user_text: str,
    ai_messages: list[dict],
    provider_status: str,
    response_source: str,
    reply: str,
    fallback_reason: str = "",
) -> None:
    if not settings.DEBUG:
        return
    logger.info(
        "AI pipeline source=%s provider_status=%s fallback_reason=%s latest=%r messages=%s reply_preview=%r",
        response_source,
        provider_status,
        fallback_reason,
        user_text,
        summarize_ai_messages(ai_messages),
        reply[:120],
    )


def significant_words(text: str) -> set[str]:
    words = []
    for raw_word in text.lower().split():
        word = "".join(character for character in raw_word if character.isalnum())
        if len(word) >= 4:
            words.append(word)
    return set(words)


def is_repetitive_provider_reply(chat: Chat, reply: str) -> bool:
    last_bot_message = chat.messages.filter(role=Message.ROLE_BOT).order_by("-created_at").first()
    if not last_bot_message:
        return False

    current = reply.strip().lower()
    previous = last_bot_message.text.strip().lower()
    if not current or not previous:
        return False
    if current == previous:
        return True

    current_words = significant_words(current)
    previous_words = significant_words(previous)
    if len(current_words) < 6 or len(previous_words) < 6:
        return False

    overlap = len(current_words & previous_words) / max(len(current_words), 1)
    similar_length = abs(len(current) - len(previous)) <= 80
    return overlap >= 0.95 and similar_length


def persona_contextual_reply(
    user_text: str,
    language: str,
    persona: str = "",
    recent_texts: list[str] | None = None,
) -> str:
    if language != "id":
        return ""

    text = user_text.lower().strip()
    recent_texts = recent_texts or []
    style = infer_persona_style(persona)

    if is_casual_embarrassment(text):
        if style == "chill_bestie":
            return "WKWKWK aduh malu banget itu, pasti langsung pengen pura-pura ada urusan lain 😭 tapi serius, salah masuk kelas tuh kejadian manusiawi banget."
        if style == "soft_listener":
            return "Yahh... malu banget ya rasanya. Tapi itu kejadian yang manusiawi banget kok, dan biasanya orang lain nggak mengingatnya selama yang kita takutkan."
        if style == "chaos_friend":
            return "ANJIR 😭 salah masuk kelas tuh paniknya beda level, pasti langsung pengen teleport keluar WKWK. Malu sih, tapi itu lucu banget kalau udah lewat."
        if style == "mature_older_friend":
            return "Wah, itu memang bikin salah tingkah. Tapi kejadian seperti itu biasanya terasa jauh lebih besar di kepala kita daripada di mata orang lain."
        return "WKWK aduh, salah masuk kelas tuh malu banget sih. Tapi itu kejadian yang manusiawi banget, dan biasanya orang lain cepat lupa kok."

    if is_casual_mishap(text):
        if style == "chill_bestie":
            return "WKWK aduh, jatuhnya tipe yang bikin malu dulu baru sakit belakangan ya. Tapi serius, kejadian kayak gitu nyebelin tapi manusiawi banget."
        if style == "soft_listener":
            return "Yah... pasti kaget dan malu juga ya. Semoga badanmu aman. Kadang momen kecil kayak gitu memang bisa kebawa kepikiran sebentar."
        if style == "chaos_friend":
            return "YAAMPUN jatuh tuh antara sakit sama malu rebutan duluan WKWK. Semoga kamu nggak kenapa-kenapa ya, tapi aku paham banget paniknya."
        if style == "mature_older_friend":
            return "Aduh, itu pasti bikin kaget. Semoga tubuhmu baik-baik saja. Kalau masih malu, wajar, tapi momen seperti itu biasanya cepat lewat."
        return "WKWK aduh, jatuh kayak gitu pasti bikin kaget dan malu. Semoga kamu nggak kenapa-kenapa ya."

    if is_sleep_followup(text) and recent_mentions_exhaustion(recent_texts):
        if style == "chill_bestie":
            return "Lah pantes makin capek WKWK. Badan udah minta istirahat, tapi kepala masih nyala terus ya. Itu kombinasi yang bikin energi habis banget."
        if style == "soft_listener":
            return "Hmm... pantes kamu makin lelah. Kalau tidur juga terganggu, tubuh dan pikiranmu jadi nggak punya ruang buat benar-benar pulih."
        if style == "chaos_friend":
            return "YAAMPUN pantes capeknya dobel 😭 badan tepar, otak malah lembur. Itu bukan malas, itu sistemmu lagi overload."
        if style == "mature_older_friend":
            return "Itu menjelaskan kenapa capeknya terasa menumpuk. Saat tidur terganggu, pikiran jadi lebih mudah berat. Kita perlu pelan-pelan turunkan bebannya dulu."
        return "Pantes kamu makin capek. Kalau tidur juga terganggu, badan dan pikiran jadi nggak benar-benar dapat waktu buat pulih."

    return ""


def local_supportive_reply(
    user_text: str,
    language: str,
    text_emotion: dict,
    persona: str = "",
    recent_texts: list[str] | None = None,
) -> str:
    """Minimal fallback used ONLY when the LLM API genuinely fails.

    This function should NOT act as a response router or keyword matcher.
    It provides a short, varied, generic fallback so the user is not left
    without any reply when the AI provider is down.
    """
    import random

    if is_simple_greeting(user_text):
        return greeting_reply(language, persona)

    if language == "en":
        return random.choice([
            "I\'m sorry, I had a brief hiccup. Could you say that again?",
            "Hmm, something went wrong on my end. Can you repeat that?",
            "I missed that\u2014mind saying it one more time?",
            "Sorry about that! Please try sending your message again.",
        ])
    return random.choice([
        "Maaf, tadi ada sedikit gangguan. Bisa coba kirim ulang pesanmu?",
        "Hmm, ada kendala sebentar. Coba ulangi pesanmu ya?",
        "Maaf, aku sempat error tadi. Kirim ulang ya biar aku bisa baca.",
        "Wah, maaf tadi ada gangguan teknis. Coba kirim lagi pesannya?",
    ])


def save_chat_exchange(
    user,
    payload: dict,
    user_text: str,
    text_emotion: dict,
    reply: str,
    face_emotion: str = "",
) -> tuple[Chat, Message]:
    with transaction.atomic():
        chat = get_or_create_chat(user, payload.get("chat_id"), user_text)
        user_message = Message.objects.create(
            chat=chat,
            role=Message.ROLE_USER,
            text=user_text,
            face_emotion=face_emotion,
            text_emotion=text_emotion["emotion"],
            mood_score=text_emotion["mood_score"],
        )
        MoodEntry.objects.create(
            user=user,
            emotion=text_emotion["emotion"],
            intensity=text_emotion["intensity"],
            source=MoodEntry.SOURCE_COMBINED if face_emotion else MoodEntry.SOURCE_TEXT,
            note=user_text[:200],
        )
        Message.objects.create(chat=chat, role=Message.ROLE_BOT, text=reply)
        if chat.messages.count() <= 2:
            chat.title = truncate_title(user_text)
        chat.save(update_fields=["title", "updated_at"])
    return chat, user_message


def process_chat_message(user, payload: dict) -> dict:
    user_text = payload["message"].strip()
    language = payload.get("language") or user.language or "id"
    face_emotion = payload.get("face_emotion", "").strip()

    if not user_text:
        return {"reply": "Hai, mau ngobrol soal apa?", "text_emotion": None}

    risk = risk_level(user_text, language)
    if risk in {"high", "medium"}:
        return {"reply": crisis_message(language), "text_emotion": None, "is_crisis": True}

    if is_policy_violation(user_text):
        return {
            "reply": policy_violation_message(language),
            "text_emotion": None,
            "locked": True,
            "is_voice": payload.get("is_voice", False),
        }

    text_emotion = detect_text_emotion(user_text, language)
    existing_chat = Chat.objects.filter(id=payload.get("chat_id"), user=user).first() if payload.get("chat_id") else None
    recent_texts = recent_user_texts(existing_chat)
    off_topic = is_off_topic(user_text)

    with transaction.atomic():
        chat = get_or_create_chat(user, payload.get("chat_id"), user_text)
        user_message = Message.objects.create(
            chat=chat,
            role=Message.ROLE_USER,
            text=user_text,
            face_emotion=face_emotion,
            text_emotion=text_emotion["emotion"],
            mood_score=text_emotion["mood_score"],
        )
        MoodEntry.objects.create(
            user=user,
            emotion=text_emotion["emotion"],
            intensity=text_emotion["intensity"],
            source=MoodEntry.SOURCE_COMBINED if face_emotion else MoodEntry.SOURCE_TEXT,
            note=user_text[:200],
        )

    system_prompt = build_persona_prompt(user, language, face_emotion, text_emotion)
    ai_messages = build_messages(chat, system_prompt, user_text, language, off_topic=off_topic)
    provider_result = generate_chat_reply_result(ai_messages, language)
    fallback_reason = provider_result.fallback_reason
    if provider_result.reply:
        reply = provider_result.reply
        response_source = "groq"
    else:
        reply = local_supportive_reply(user_text, language, text_emotion, user.ai_persona, recent_texts)
        response_source = "local_fallback"

    log_generation_debug(
        user_text=user_text,
        ai_messages=ai_messages,
        provider_status=provider_result.status,
        response_source=response_source,
        reply=reply,
        fallback_reason=fallback_reason,
    )

    with transaction.atomic():
        Message.objects.create(chat=chat, role=Message.ROLE_BOT, text=reply)
        if chat.messages.count() <= 2:
            chat.title = truncate_title(user_text)
        chat.save(update_fields=["title", "updated_at"])

    return {
        "reply": reply,
        "chat_id": chat.id,
        "message_id": user_message.id,
        "text_emotion": text_emotion,
        "is_voice": payload.get("is_voice", False),
        "response_source": response_source,
        "fallback_reason": fallback_reason,
    }
