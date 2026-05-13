"""
HelloMind — Text-based Emotion Detection
Keyword-based approach for fast, offline emotion classification.
"""

# Emotion keyword maps (Indonesian + English)
EMOTION_KEYWORDS = {
    "happy": {
        "id": [
            "senang", "bahagia", "gembira", "seru", "asik", "asyik", "keren",
            "yeay", "hore", "mantap", "semangat", "bangga", "sukses", "berhasil",
            "seneng", "hepi", "happy", "excited", "lucu", "ketawa", "ngakak",
            "terharu", "bersyukur", "syukur", "alhamdulillah", "makasih",
            "cinta", "sayang", "suka", "love", "lega", "puas", "tenang",
        ],
        "en": [
            "happy", "glad", "joyful", "excited", "awesome", "great", "wonderful",
            "amazing", "love", "grateful", "thankful", "proud", "delighted",
            "cheerful", "thrilled", "fantastic", "blessed", "celebrate",
            "fun", "laugh", "smile", "relieved", "peaceful", "calm",
        ],
    },
    "sad": {
        "id": [
            "sedih", "nangis", "menangis", "galau", "patah hati", "kecewa",
            "kehilangan", "rindu", "kangen", "sendiri", "sendirian", "sepi",
            "hampa", "kosong", "pilu", "nelangsa", "down", "murung",
            "terpuruk", "gagal", "menyesal", "nyesel", "sakit hati",
            "ditinggal", "broken", "rapuh", "lemah", "capek", "cape",
            "lelah", "putus asa", "hopeless", "nggak bisa", "ga bisa",
        ],
        "en": [
            "sad", "crying", "heartbroken", "disappointed", "lonely", "alone",
            "empty", "lost", "miss", "depressed", "down", "hopeless",
            "failed", "regret", "hurt", "pain", "broken", "weak",
            "tired", "exhausted", "overwhelmed", "helpless", "miserable",
        ],
    },
    "angry": {
        "id": [
            "marah", "kesal", "jengkel", "benci", "muak", "emosi",
            "geram", "sebel", "sebal", "gondok", "dongkol", "frustrasi",
            "ngeselin", "nyebelin", "kampret", "sialan", "bangsat",
            "nggak adil", "ga adil", "keterlaluan", "kurang ajar",
            "ngamuk", "berantem", "ribut",
        ],
        "en": [
            "angry", "mad", "furious", "annoyed", "irritated", "hate",
            "frustrated", "rage", "pissed", "upset", "disgusted",
            "unfair", "outrageous", "terrible",
        ],
    },
    "anxious": {
        "id": [
            "cemas", "khawatir", "takut", "panik", "gelisah", "gugup",
            "nervous", "was-was", "waswas", "deg-degan", "bingung",
            "overthinking", "kepikiran", "insecure", "minder",
            "nggak tenang", "ga tenang", "stress", "stres", "tertekan",
            "nggak bisa tidur", "ga bisa tidur", "insomnia",
            "paranoid", "trauma", "ngeri",
        ],
        "en": [
            "anxious", "worried", "scared", "afraid", "panic", "nervous",
            "restless", "uneasy", "stressed", "overwhelmed", "insecure",
            "overthinking", "paranoid", "terrified", "tense",
        ],
    },
}

# Intensity boosters
INTENSIFIERS = {
    "id": [
        "banget", "sangat", "amat", "bgt", "parah", "poll", "pol",
        "super", "luar biasa", "extreme", "mati-matian", "bener-bener",
        "beneran", "serius", "nggak kuat", "ga kuat", "udah", "terus-terusan",
    ],
    "en": [
        "very", "extremely", "so", "really", "incredibly", "absolutely",
        "completely", "totally", "deeply", "seriously", "constantly",
    ],
}

# Mood score mapping
MOOD_SCORES = {
    "happy": 0.8,
    "sad": -0.6,
    "angry": -0.5,
    "anxious": -0.4,
    "neutral": 0.0,
}


def detect_text_emotion(text: str, lang: str = "id") -> dict:
    """
    Analyze text to detect emotion.

    Returns: {
        "emotion": str,       # happy, sad, angry, anxious, neutral
        "intensity": int,     # 1-5
        "confidence": float,  # 0.0-1.0
        "mood_score": float,  # -1.0 to 1.0
    }
    """
    t = text.lower().strip()
    if not t:
        return {
            "emotion": "neutral",
            "intensity": 1,
            "confidence": 0.0,
            "mood_score": 0.0,
        }

    # Count keyword matches per emotion
    scores = {}
    for emotion, kw_map in EMOTION_KEYWORDS.items():
        keywords = kw_map.get(lang, []) + kw_map.get("id" if lang == "en" else "en", [])
        count = sum(1 for kw in keywords if kw in t)
        if count > 0:
            scores[emotion] = count

    if not scores:
        return {
            "emotion": "neutral",
            "intensity": 1,
            "confidence": 0.3,
            "mood_score": 0.0,
        }

    # Pick dominant emotion
    dominant = max(scores, key=scores.get)
    match_count = scores[dominant]

    # Calculate intensity based on match count + intensifiers
    intensifier_words = INTENSIFIERS.get(lang, []) + INTENSIFIERS.get("id" if lang == "en" else "en", [])
    intensifier_count = sum(1 for w in intensifier_words if w in t)

    base_intensity = min(match_count, 3)  # 1-3 from keywords
    boost = min(intensifier_count, 2)     # 0-2 from intensifiers
    intensity = min(base_intensity + boost, 5)
    intensity = max(intensity, 1)

    # Confidence based on how many keywords matched
    total_possible = len(EMOTION_KEYWORDS[dominant].get(lang, []))
    confidence = min(match_count / max(total_possible * 0.3, 1), 1.0)
    confidence = round(confidence, 2)

    # Mood score
    mood = MOOD_SCORES.get(dominant, 0.0)
    # Adjust mood by intensity
    mood = mood * (intensity / 3.0)
    mood = max(-1.0, min(1.0, round(mood, 2)))

    return {
        "emotion": dominant,
        "intensity": intensity,
        "confidence": confidence,
        "mood_score": mood,
    }
