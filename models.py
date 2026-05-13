"""
HelloMind — Database Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    language = Column(String(5), default="id")  # "id" or "en"
    ai_name = Column(String(50), default="HelloMind")
    ai_persona = Column(Text, default="Kamu adalah AI pendamping kesehatan mental yang empatik, ramah, dan suportif.")
    created_at = Column(DateTime, default=datetime.utcnow)

    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    mood_entries = relationship("MoodEntry", back_populates="user", cascade="all, delete-orphan")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), default="Obrolan Baru")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan",
                            order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "bot"
    text = Column(Text, nullable=False)
    face_emotion = Column(String(20), default="")
    text_emotion = Column(String(20), default="")
    mood_score = Column(Float, default=0.0)  # -1.0 (very negative) to 1.0 (very positive)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")


class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    emotion = Column(String(20), nullable=False)  # happy, sad, angry, anxious, neutral
    intensity = Column(Integer, default=3)  # 1-5
    source = Column(String(20), default="text")  # "text", "face", "combined"
    note = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="mood_entries")
