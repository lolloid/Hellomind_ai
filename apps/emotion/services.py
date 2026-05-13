EMOTION_KEYWORDS = {
    "happy": {
        "id": ["senang", "bahagia", "gembira", "seru", "asyik", "bangga", "berhasil", "seneng", "happy", "lega", "tenang"],
        "en": ["happy", "glad", "joyful", "excited", "great", "proud", "relieved", "peaceful", "calm"],
    },
    "sad": {
        "id": ["sedih", "nangis", "galau", "kecewa", "sendiri", "sendirian", "sepi", "hampa", "down", "capek", "lelah", "putus asa"],
        "en": ["sad", "crying", "heartbroken", "lonely", "alone", "empty", "depressed", "down", "hopeless", "tired", "exhausted"],
    },
    "angry": {
        "id": ["marah", "kesal", "jengkel", "benci", "muak", "emosi", "frustrasi", "sebel", "nggak adil", "ga adil"],
        "en": ["angry", "mad", "furious", "annoyed", "irritated", "hate", "frustrated", "unfair", "upset"],
    },
    "anxious": {
        "id": ["cemas", "khawatir", "takut", "panik", "gelisah", "gugup", "overthinking", "kepikiran", "stress", "stres", "insomnia"],
        "en": ["anxious", "worried", "scared", "afraid", "panic", "nervous", "stressed", "overthinking", "tense"],
    },
}

INTENSIFIERS = {
    "id": ["banget", "sangat", "amat", "bgt", "parah", "super", "bener-bener", "serius", "nggak kuat", "ga kuat"],
    "en": ["very", "extremely", "so", "really", "incredibly", "absolutely", "seriously", "constantly"],
}

MOOD_SCORES = {
    "happy": 0.8,
    "sad": -0.6,
    "angry": -0.5,
    "anxious": -0.4,
    "neutral": 0.0,
}


def detect_text_emotion(text: str, language: str = "id") -> dict:
    value = text.lower().strip()
    if not value:
        return {"emotion": "neutral", "intensity": 1, "confidence": 0.0, "mood_score": 0.0}

    fallback_language = "en" if language == "id" else "id"
    scores = {}
    for emotion, keyword_map in EMOTION_KEYWORDS.items():
        keywords = keyword_map.get(language, []) + keyword_map.get(fallback_language, [])
        matches = sum(1 for keyword in keywords if keyword in value)
        if matches:
            scores[emotion] = matches

    if not scores:
        return {"emotion": "neutral", "intensity": 1, "confidence": 0.3, "mood_score": 0.0}

    dominant = max(scores, key=scores.get)
    match_count = scores[dominant]
    intensifiers = INTENSIFIERS.get(language, []) + INTENSIFIERS.get(fallback_language, [])
    intensifier_count = sum(1 for keyword in intensifiers if keyword in value)

    intensity = min(max(min(match_count, 3) + min(intensifier_count, 2), 1), 5)
    total_possible = len(EMOTION_KEYWORDS[dominant].get(language, []))
    confidence = round(min(match_count / max(total_possible * 0.3, 1), 1.0), 2)
    mood_score = round(max(-1.0, min(1.0, MOOD_SCORES.get(dominant, 0.0) * (intensity / 3.0))), 2)

    return {
        "emotion": dominant,
        "intensity": intensity,
        "confidence": confidence,
        "mood_score": mood_score,
    }
