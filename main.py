import os
import sys
import logging
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
import traceback

from persona import BASE_PERSONA
from safety import check_risk, CRISIS_MESSAGE

# Logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("hellomind")

# ======================
# KONFIGURASI GROQ (OpenAI-compatible)
# ======================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY belum diset di file .env")

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


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    traceback.print_exc(file=sys.stdout)
    return JSONResponse(
        status_code=500,
        content={"reply": "Maaf, ada kesalahan internal. Coba lagi ya."}
    )


# ======================
# REQUEST MODEL
# ======================
class ChatMessage(BaseModel):
    role: str
    text: str


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

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


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

    try:
        logger.info(f"Calling Groq API with {len(messages)} messages...")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            max_tokens=500,
        )

        reply = response.choices[0].message.content.strip()
        logger.info(f"Got reply: {reply[:50]}...")

        # Fallback kalau respons kosong
        if not reply:
            reply = "Hmm, coba ceritain lagi? Aku pengin ngerti."

    except Exception as e:
        logger.error(f"API Error: {e}")
        traceback.print_exc(file=sys.stdout)
        reply = "Maaf, lagi ada gangguan teknis. Coba lagi sebentar ya."

    return JSONResponse({"reply": reply})


@app.post("/mood")
def mood_endpoint(req: MoodRequest):
    """Track mood (stored client-side, this just validates)."""
    valid_moods = ["senang", "biasa", "sedih", "cemas", "marah"]
    if req.mood.lower() not in valid_moods:
        return JSONResponse({"status": "error", "message": "Mood tidak valid"})
    return JSONResponse({"status": "ok", "mood": req.mood.lower()})
