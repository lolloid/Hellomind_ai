<<<<<<< HEAD
"""
HelloMind — Safety Module (Multi-language: ID & EN)
"""

DANGER_KEYWORDS_ID = [
    # eksplisit
    "bunuh diri", "ingin mati", "pengen mati", "pengin mati", "mau mati",
    "gantung diri", "self harm", "menyakiti diri", "overdosis",
    "loncat dari", "potong nadi", "minum racun",
    # implisit
    "nggak mau hidup", "tidak mau hidup", "ga mau hidup", "gak mau hidup lagi",
    "capek hidup", "cape hidup", "bosen hidup", "bosan hidup",
    "ingin menghilang", "pengen hilang", "pengin hilang",
    "hidup nggak ada gunanya", "hidup ga ada gunanya", "hidup gak ada gunanya",
    "hidup tidak ada gunanya", "lebih baik nggak ada", "lebih baik ga ada",
    "kalau aku nggak ada", "kalau aku ga ada",
    "pengen tidur terus", "pengin tidur terus",
    "nggak pengen bangun", "nggak pengin bangun",
    "udah nggak kuat hidup", "udah gak kuat hidup",
    "ngerasa nggak berarti", "ngerasa gak berarti",
    "dunia tanpa aku", "lebih baik mati", "mending mati",
    "nyesel hidup", "nyesel lahir",
    "pengen akhiri", "pengin akhiri", "akhiri semuanya",
    "akhiri hidupku", "selesaiin hidupku",
]

HIGH_RISK_ID = [
    "bunuh diri", "gantung diri", "overdosis", "loncat dari",
    "potong nadi", "minum racun", "ingin mati", "pengen mati",
    "pengin mati", "mau mati", "lebih baik mati", "mending mati",
    "akhiri hidupku", "selesaiin hidupku",
]

DANGER_KEYWORDS_EN = [
    # explicit
    "kill myself", "want to die", "wanna die", "end my life", "suicide",
    "hang myself", "self harm", "self-harm", "cut myself", "overdose",
    "jump off", "slit my wrists", "drink poison",
    # implicit
    "don't want to live", "dont want to live", "tired of living",
    "want to disappear", "wanna disappear",
    "life is meaningless", "life is pointless", "life has no meaning",
    "better off without me", "better off dead",
    "wish i was never born", "wish i wasn't born",
    "can't take it anymore", "cant take it anymore",
    "want to sleep forever", "never wake up",
    "i'm worthless", "im worthless", "i am worthless",
    "world without me", "end it all", "end everything",
    "no reason to live", "nothing to live for",
]

HIGH_RISK_EN = [
    "kill myself", "suicide", "hang myself", "overdose",
    "jump off", "slit my wrists", "drink poison",
    "want to die", "wanna die", "end my life",
    "better off dead", "end it all",
]


def risk_level(text: str, lang: str = "id") -> str:
    """Determine risk level: 'high', 'medium', or 'low'."""
    t = text.lower()

    # Check both languages always for safety
    high_risk = HIGH_RISK_ID + HIGH_RISK_EN
    danger_keywords = DANGER_KEYWORDS_ID + DANGER_KEYWORDS_EN

    if any(k in t for k in high_risk):
        return "high"
    if any(k in t for k in danger_keywords):
=======
DANGER_KEYWORDS = [
    # eksplisit
    "bunuh diri",
    "ingin mati",
    "pengen mati",
    "pengin mati",
    "mau mati",
    "gantung diri",
    "self harm",
    "menyakiti diri",
    "overdosis",
    "loncat dari",
    "potong nadi",
    "minum racun",

    # implisit / tidak langsung
    "nggak mau hidup",
    "tidak mau hidup",
    "ga mau hidup",
    "gak mau hidup lagi",
    "capek hidup",
    "cape hidup",
    "bosen hidup",
    "bosan hidup",
    "ingin menghilang",
    "pengen hilang",
    "pengin hilang",
    "hidup nggak ada gunanya",
    "hidup ga ada gunanya",
    "hidup gak ada gunanya",
    "hidup tidak ada gunanya",
    "lebih baik nggak ada",
    "lebih baik ga ada",
    "kalau aku nggak ada",
    "kalau aku ga ada",
    "pengen tidur terus",
    "pengin tidur terus",
    "nggak pengen bangun",
    "nggak pengin bangun",
    "udah nggak kuat hidup",
    "udah gak kuat hidup",
    "ngerasa nggak berarti",
    "ngerasa gak berarti",
    "dunia tanpa aku",
    "lebih baik mati",
    "mending mati",
    "nyesel hidup",
    "nyesel lahir",
    "pengen akhiri",
    "pengin akhiri",
    "akhiri semuanya",
    "akhiri hidupku",
    "selesaiin hidupku",
]

HIGH_RISK = [
    "bunuh diri",
    "gantung diri",
    "overdosis",
    "loncat dari",
    "potong nadi",
    "minum racun",
    "ingin mati",
    "pengen mati",
    "pengin mati",
    "mau mati",
    "lebih baik mati",
    "mending mati",
    "akhiri hidupku",
    "selesaiin hidupku",
]


def risk_level(text: str) -> str:
    """Menentukan level risiko: 'high', 'medium', atau 'low'."""
    t = text.lower()
    if any(k in t for k in HIGH_RISK):
        return "high"
    if any(k in t for k in DANGER_KEYWORDS):
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
        return "medium"
    return "low"


<<<<<<< HEAD
def check_risk(text: str, lang: str = "id") -> bool:
    """Return True if danger indicators are detected."""
    return risk_level(text, lang) in ("high", "medium")


CRISIS_MESSAGE_ID = (
=======
def check_risk(text: str) -> bool:
    """Return True jika terdeteksi ada indikasi bahaya."""
    return risk_level(text) in ("high", "medium")


CRISIS_MESSAGE = (
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
    "Aku bener-bener dengerin kamu, dan aku khawatir.\n\n"
    "Aku cuma bisa nemenin lewat obrolan, "
    "tapi kondisi kayak gini butuh bantuan dari orang yang benar-benar bisa bantu.\n\n"
    "Kalau kamu di Indonesia, kamu bisa hubungi:\n"
    "📞 119 ext. 8 — Hotline Kesehatan Jiwa\n"
    "📞 021-500-454 — Into The Light Indonesia\n"
    "📞 Atau hubungi orang terdekat yang kamu percaya\n\n"
    "Kalau kamu di luar Indonesia, hubungi layanan darurat setempat.\n"
    "Kamu nggak harus ngadepin ini sendirian. Aku masih di sini."
)
<<<<<<< HEAD

CRISIS_MESSAGE_EN = (
    "I hear you, and I'm really concerned about what you're going through.\n\n"
    "I can be here to chat, "
    "but what you're feeling right now deserves support from someone who can truly help.\n\n"
    "Please reach out to:\n"
    "📞 988 Suicide & Crisis Lifeline (US)\n"
    "📞 116 123 — Samaritans (UK)\n"
    "📞 Or contact your local emergency services\n\n"
    "You don't have to face this alone. I'm still here for you."
)

# Backward compatibility
CRISIS_MESSAGE = CRISIS_MESSAGE_ID


def get_crisis_message(lang: str = "id") -> str:
    """Get crisis message in the appropriate language."""
    if lang == "en":
        return CRISIS_MESSAGE_EN
    return CRISIS_MESSAGE_ID


JAILBREAK_KEYWORDS = [
    # Prompt injection / Bypass
    "ignore previous", "abaikan instruksi", "ubah peran", "kamu adalah asisten",
    "kamu sekarang", "jadilah", "system prompt", "berpura-puralah", "pretend",
    "forget previous", "lupakan instruksi", "bertindak sebagai", "act as",
    "bypass", "jailbreak", "aturan", "rules", "developer mode", "dan mode"
]

PORN_KEYWORDS = [
    # Pornography / Sexual Content
    "porn", "sex", "seks", "ngentot", "kontol", "memek", "bokep", "bugil",
    "telanjang", "desah", "sange", "nude", "horny", "masturbasi", "colmek",
    "roleplay sex", "rp sex", "desahan", "binal", "mesum"
]

OFFTOPIC_KEYWORDS = [
    # Coding / Tech
    "coding", "code", "python", "javascript", "html", "css", "sql", "bug", "debug", 
    "script", "bantu coding", "buatkan kode", "bikin script", "tolong kode", 
    "bantu tugas", "bantu pr", "kerjakan tugas", "buat program", "buat web",
    "write code", "fix bug", "programming", "teknis", "hack", "hacking"
]

def check_jailbreak_or_porn(text: str) -> bool:
    """Return True if severe violation (jailbreak or porn) is detected."""
    t = text.lower()
    return any(k in t for k in JAILBREAK_KEYWORDS + PORN_KEYWORDS)

def check_off_topic(text: str) -> bool:
    """Return True if harmless off-topic (tech/coding) is detected."""
    t = text.lower()
    return any(k in t for k in OFFTOPIC_KEYWORDS)

JAILBREAK_MESSAGE_ID = "Maaf, sistem mendeteksi adanya indikasi pelanggaran kebijakan, eksploitasi, atau percakapan yang tidak pantas (seperti unsur seksual/bypass). Obrolan ini aku tutup sekarang ya. Silakan buat obrolan baru jika ingin mengobrol secara normal."
JAILBREAK_MESSAGE_EN = "I'm sorry, the system detected a policy violation, exploitation, or inappropriate conversation (such as sexual content or bypass attempts). I am locking this chat now. Please start a new chat to continue normally."

OFFTOPIC_MESSAGE_ID = "Maaf ya, aku cuma di sini sebagai teman ngobrol buat dengerin cerita kamu. Aku nggak bisa bantu urusan teknis, ngerjain tugas, coding, atau hal-hal di luar itu. Ada hal lain yang lagi kamu rasain dan mau diceritain?"
OFFTOPIC_MESSAGE_EN = "I'm sorry, I'm only here to be a listening friend for your personal feelings. I can't assist with technical tasks, coding, or homework. Is there anything else on your mind you'd like to share?"

def get_jailbreak_message(lang: str = "id") -> str:
    if lang == "en":
        return JAILBREAK_MESSAGE_EN
    return JAILBREAK_MESSAGE_ID

def get_offtopic_message(lang: str = "id") -> str:
    if lang == "en":
        return OFFTOPIC_MESSAGE_EN
    return OFFTOPIC_MESSAGE_ID

=======
>>>>>>> 27e88cda7da66357dfcba746088dfc3c90b0c9d0
