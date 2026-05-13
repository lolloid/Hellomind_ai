<<<<<<< HEAD
"""
HelloMind — Main Application (v3.0)
FastAPI backend with auth, database, text emotion, multi-language, and mood tracking.
"""
import os
import sys
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Depends, HTTPException, status
=======
import os
import sys
import logging
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
<<<<<<< HEAD
from sqlalchemy.orm import Session
from sqlalchemy import func
import traceback

from database import get_db, init_db
from models import User, Chat, Message, MoodEntry
from auth import (
    hash_password, verify_password, create_token, get_current_user
)
from persona import get_persona
from safety import check_risk, get_crisis_message, risk_level, check_jailbreak_or_porn, get_jailbreak_message
from text_emotion import detect_text_emotion
=======
import traceback

from persona import BASE_PERSONA
from safety import check_risk, CRISIS_MESSAGE
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0

# Logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("hellomind")

# ======================
<<<<<<< HEAD
# KONFIGURASI GROQ
=======
# KONFIGURASI GROQ (OpenAI-compatible)
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
# ======================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY belum diset di file .env")

<<<<<<< HEAD
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    timeout=15.0,  # Prevent hanging requests
)

# ======================
# APP
# ======================
app = FastAPI(title="HelloMind", version="3.0")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    init_db()
    logger.info("Database initialized successfully")


=======
# Groq menyediakan endpoint yang kompatibel dengan OpenAI SDK
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


# ======================
# APP
# ======================
app = FastAPI(title="HelloMind", version="2.0")
app.mount("/static", StaticFiles(directory="static"), name="static")


>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    traceback.print_exc(file=sys.stdout)
    return JSONResponse(
        status_code=500,
<<<<<<< HEAD
        content={"detail": "Maaf, ada kesalahan internal. Coba lagi ya."}
=======
        content={"reply": "Maaf, ada kesalahan internal. Coba lagi ya."}
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
    )


# ======================
<<<<<<< HEAD
# REQUEST MODELS
# ======================
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class SettingsRequest(BaseModel):
    language: str = "id"
    ai_name: Optional[str] = None
    ai_persona: Optional[str] = None

=======
# REQUEST MODEL
# ======================
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
class ChatMessage(BaseModel):
    role: str
    text: str

<<<<<<< HEAD
class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    face_emotion: str = ""
    chat_id: Optional[int] = None
    language: str = "id"
    is_voice: bool = False

class ChatCreateRequest(BaseModel):
    title: str = "Obrolan Baru"

class ChatRenameRequest(BaseModel):
    title: str


# ======================
# PAGES
# ======================
=======

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    mood: Optional[str] = None


class MoodRequest(BaseModel):
    mood: str
    note: Optional[str] = None


# ======================
# ROUTES
# ======================

>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

<<<<<<< HEAD
@app.get("/login", response_class=HTMLResponse)
def serve_login():
    with open("static/login.html", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    with open("static/dashboard.html", encoding="utf-8") as f:
        return f.read()


# ======================
# AUTH ENDPOINTS
# ======================
@app.post("/auth/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # Check existing
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=400, detail="Username sudah dipakai.")
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email sudah terdaftar.")
    if len(req.password) < 4:
        raise HTTPException(status_code=400, detail="Password minimal 4 karakter.")

    user = User(
        username=req.username,
        email=req.email,
        password_hash=hash_password(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id, user.username)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "language": user.language,
            "ai_name": user.ai_name,
            "ai_persona": user.ai_persona,
        }
    }


@app.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Username atau password salah.")

    token = create_token(user.id, user.username)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "language": user.language,
            "ai_name": user.ai_name,
            "ai_persona": user.ai_persona,
        }
    }


@app.get("/auth/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "language": user.language,
        "ai_name": user.ai_name,
        "ai_persona": user.ai_persona,
    }


@app.put("/auth/settings")
def update_settings(
    req: SettingsRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user.language = req.language
    if req.ai_name is not None:
        user.ai_name = req.ai_name
    if req.ai_persona is not None:
        user.ai_persona = req.ai_persona
    db.commit()
    return {
        "message": "Settings updated", 
        "language": user.language,
        "ai_name": user.ai_name,
        "ai_persona": user.ai_persona
    }


# ======================
# CHAT CRUD
# ======================
@app.get("/chats")
def list_chats(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chats = (
        db.query(Chat)
        .filter(Chat.user_id == user.id)
        .order_by(Chat.updated_at.desc())
        .all()
    )
    return [
        {
            "id": c.id,
            "title": c.title,
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat(),
            "message_count": len(c.messages),
        }
        for c in chats
    ]


@app.post("/chats")
def create_chat(
    req: ChatCreateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = Chat(user_id=user.id, title=req.title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return {
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at.isoformat(),
    }


@app.delete("/chats/{chat_id}")
def delete_chat(
    chat_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat tidak ditemukan.")
    db.delete(chat)
    db.commit()
    return {"message": "Chat dihapus."}


@app.put("/chats/{chat_id}")
def rename_chat(
    chat_id: int,
    req: ChatRenameRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat tidak ditemukan.")
    chat.title = req.title
    db.commit()
    return {"message": "Chat renamed.", "title": chat.title}


@app.get("/chats/{chat_id}/messages")
def get_messages(
    chat_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat tidak ditemukan.")
    return [
        {
            "id": m.id,
            "role": m.role,
            "text": m.text,
            "face_emotion": m.face_emotion,
            "text_emotion": m.text_emotion,
            "mood_score": m.mood_score,
            "created_at": m.created_at.isoformat(),
        }
        for m in chat.messages
    ]


# ======================
# CHAT ENDPOINT (with auth + DB + text emotion)
# ======================
@app.post("/chat")
def chat_endpoint(
    req: ChatRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_text = req.message.strip()
    lang = req.language or user.language or "id"
    logger.info(f"[{user.username}] {user_text[:50]}...")

    if not user_text:
        return JSONResponse({"reply": "Hai, mau ngobrol soal apa?", "text_emotion": None})

    # Safety check
    r = risk_level(user_text, lang)
    if r in ("high", "medium"):
        crisis_msg = get_crisis_message(lang)
        return JSONResponse({"reply": crisis_msg, "text_emotion": None, "is_crisis": True})

    # Jailbreak & Porn check (Locks chat)
    if check_jailbreak_or_porn(user_text):
        jailbreak_msg = get_jailbreak_message(lang)
        return JSONResponse({"reply": jailbreak_msg, "text_emotion": None, "locked": True, "is_voice": req.is_voice})

    # Text emotion detection
    text_emo = detect_text_emotion(user_text, lang)

    # Get or create chat
    chat = None
    if req.chat_id:
        chat = db.query(Chat).filter(Chat.id == req.chat_id, Chat.user_id == user.id).first()
    if not chat:
        chat = Chat(user_id=user.id, title=user_text[:32] + ("…" if len(user_text) > 32 else ""))
        db.add(chat)
        db.commit()
        db.refresh(chat)

    # Save user message
    user_msg = Message(
        chat_id=chat.id,
        role="user",
        text=user_text,
        face_emotion=req.face_emotion,
        text_emotion=text_emo["emotion"],
        mood_score=text_emo["mood_score"],
    )
    db.add(user_msg)

    # Save mood entry
    mood_entry = MoodEntry(
        user_id=user.id,
        emotion=text_emo["emotion"],
        intensity=text_emo["intensity"],
        source="combined" if req.face_emotion else "text",
        note=user_text[:200],
    )
    db.add(mood_entry)
    db.commit()

    # Build prompt
    system_prompt = get_persona(lang)

    if user.ai_persona and user.ai_persona.strip():
        system_prompt = f"USER CUSTOM PERSONA INSTRUCTIONS (Apply these to your personality):\n{user.ai_persona.strip()}\n\n---\n\n" + system_prompt

    ai_name = user.ai_name or "HelloMind"
    system_prompt = f"Your name is {ai_name}. Introduce yourself or act as {ai_name} if asked.\n\n" + system_prompt

    # Add face emotion context
    if req.face_emotion and req.face_emotion.strip():
        face_ctx = (
            f"\n\n[CRITICAL SYSTEM OVERRIDE: YOU ARE CURRENTLY CONNECTED TO THE USER'S CAMERA. "
            f"You CAN see them. Their real-time facial expression is '{req.face_emotion}'. "
            "If the user asks if you can see them or what they look like, you MUST confirm that you see them "
            "and warmly mention their expression. DO NOT say you are an AI without eyes. DO NOT mention 'kamera' or 'sistem', just act naturally like a friend looking at them.]"
        )
        system_prompt += face_ctx

    # Add text emotion context
    if text_emo["emotion"] != "neutral" and text_emo["confidence"] > 0.2:
        text_ctx = (
            f"\n\n[Context: Text emotion analysis detected '{text_emo['emotion']}' "
            f"with intensity {text_emo['intensity']}/5. "
            "Use as context, never mention analysis in response.]"
        )
        system_prompt += text_ctx

    messages = [{"role": "system", "content": system_prompt}]

    # Load previous messages from DB (max 20)
    prev_msgs = (
        db.query(Message)
        .filter(Message.chat_id == chat.id)
        .order_by(Message.created_at.desc())
        .limit(21)
        .all()
    )
    prev_msgs.reverse()

    for m in prev_msgs[:-1]:  # Exclude current message
        role = "user" if m.role == "user" else "assistant"
        messages.append({"role": role, "content": m.text})

    messages.append({"role": "user", "content": user_text})
=======

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    user_text = req.message.strip()
    logger.info(f"Received: {user_text[:50]}...")

    # Pesan kosong
    if not user_text:
        return JSONResponse({"reply": "Hai, mau ngobrol soal apa?"})

    # Safety check — prioritas utama
    if check_risk(user_text):
        return JSONResponse({"reply": CRISIS_MESSAGE})

    # Bangun messages untuk API
    messages = [{"role": "system", "content": BASE_PERSONA}]

    # Masukkan riwayat percakapan (max 20 pesan terakhir)
    for msg in req.history[-20:]:
        role = "user" if msg.role == "user" else "assistant"
        messages.append({"role": role, "content": msg.text})

    # Tambahkan mood context jika ada
    if req.mood:
        user_text_with_context = f"[Mood saat ini: {req.mood}] {user_text}"
    else:
        user_text_with_context = user_text

    # Tambahkan pesan terbaru
    messages.append({"role": "user", "content": user_text_with_context})
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0

    try:
        logger.info(f"Calling Groq API with {len(messages)} messages...")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
<<<<<<< HEAD
            temperature=0.6,
            top_p=0.9,
            max_tokens=200,
=======
            temperature=0.7,
            top_p=0.9,
            max_tokens=500,
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
        )

        reply = response.choices[0].message.content.strip()
        logger.info(f"Got reply: {reply[:50]}...")

<<<<<<< HEAD
        if not reply:
            reply = "Hmm, coba ceritain lagi? Aku pengin ngerti." if lang == "id" else "Hmm, tell me more? I want to understand."
=======
        # Fallback kalau respons kosong
        if not reply:
            reply = "Hmm, coba ceritain lagi? Aku pengin ngerti."
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0

    except Exception as e:
        logger.error(f"API Error: {e}")
        traceback.print_exc(file=sys.stdout)
<<<<<<< HEAD
        reply = "Maaf, lagi ada gangguan teknis. Coba lagi sebentar ya." if lang == "id" else "Sorry, there's a technical issue. Please try again."

    # Save bot reply
    bot_msg = Message(
        chat_id=chat.id,
        role="bot",
        text=reply,
    )
    db.add(bot_msg)

    # Update chat title if first message
    if len(prev_msgs) <= 1:
        chat.title = user_text[:32] + ("…" if len(user_text) > 32 else "")

    chat.updated_at = datetime.utcnow()
    db.commit()

    return JSONResponse({
        "reply": reply,
        "chat_id": chat.id,
        "text_emotion": text_emo,
        "is_voice": req.is_voice,
    })


# ======================
# MOOD ENDPOINTS
# ======================
@app.get("/mood/history")
def mood_history(
    days: int = 30,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=days)
    entries = (
        db.query(MoodEntry)
        .filter(MoodEntry.user_id == user.id, MoodEntry.created_at >= since)
        .order_by(MoodEntry.created_at.desc())
        .limit(500)
        .all()
    )
    return [
        {
            "id": e.id,
            "emotion": e.emotion,
            "intensity": e.intensity,
            "source": e.source,
            "note": e.note,
            "created_at": e.created_at.isoformat(),
        }
        for e in entries
    ]


@app.get("/mood/summary")
def mood_summary(
    days: int = 7,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=days)
    entries = (
        db.query(MoodEntry)
        .filter(MoodEntry.user_id == user.id, MoodEntry.created_at >= since)
        .all()
    )

    if not entries:
        return {
            "total_entries": 0,
            "emotion_counts": {},
            "avg_intensity": 0,
            "dominant_emotion": "neutral",
            "daily_moods": [],
        }

    # Count emotions
    emotion_counts = {}
    total_intensity = 0
    for e in entries:
        emotion_counts[e.emotion] = emotion_counts.get(e.emotion, 0) + 1
        total_intensity += e.intensity

    dominant = max(emotion_counts, key=emotion_counts.get)
    avg_intensity = round(total_intensity / len(entries), 1)

    # Daily mood aggregation
    daily = {}
    for e in entries:
        day = e.created_at.strftime("%Y-%m-%d")
        if day not in daily:
            daily[day] = {"emotions": [], "intensities": []}
        daily[day]["emotions"].append(e.emotion)
        daily[day]["intensities"].append(e.intensity)

    daily_moods = []
    for day, data in sorted(daily.items()):
        from collections import Counter
        most_common = Counter(data["emotions"]).most_common(1)[0][0]
        avg_int = round(sum(data["intensities"]) / len(data["intensities"]), 1)
        daily_moods.append({
            "date": day,
            "dominant_emotion": most_common,
            "avg_intensity": avg_int,
            "count": len(data["emotions"]),
        })

    return {
        "total_entries": len(entries),
        "emotion_counts": emotion_counts,
        "avg_intensity": avg_intensity,
        "dominant_emotion": dominant,
        "daily_moods": daily_moods,
    }
=======
        reply = "Maaf, lagi ada gangguan teknis. Coba lagi sebentar ya."

    return JSONResponse({"reply": reply})


@app.post("/mood")
def mood_endpoint(req: MoodRequest):
    """Track mood (stored client-side, this just validates)."""
    valid_moods = ["senang", "biasa", "sedih", "cemas", "marah"]
    if req.mood.lower() not in valid_moods:
        return JSONResponse({"status": "error", "message": "Mood tidak valid"})
    return JSONResponse({"status": "ok", "mood": req.mood.lower()})
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
