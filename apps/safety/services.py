DANGER_KEYWORDS_ID = [
    "bunuh diri", "ingin mati", "pengen mati", "pengin mati", "mau mati",
    "gantung diri", "self harm", "menyakiti diri", "overdosis",
    "loncat dari", "potong nadi", "minum racun", "nggak mau hidup",
    "tidak mau hidup", "ga mau hidup", "gak mau hidup lagi", "capek hidup",
    "cape hidup", "bosan hidup", "bosen hidup", "ingin menghilang",
    "pengen hilang", "pengin hilang", "hidup nggak ada gunanya",
    "hidup ga ada gunanya", "hidup tidak ada gunanya", "lebih baik mati",
    "mending mati", "akhiri hidupku", "selesaiin hidupku",
]

HIGH_RISK_ID = [
    "bunuh diri", "gantung diri", "overdosis", "loncat dari",
    "potong nadi", "minum racun", "ingin mati", "pengen mati",
    "pengin mati", "mau mati", "lebih baik mati", "mending mati",
    "akhiri hidupku", "selesaiin hidupku",
]

DANGER_KEYWORDS_EN = [
    "kill myself", "want to die", "wanna die", "end my life", "suicide",
    "hang myself", "self harm", "self-harm", "cut myself", "overdose",
    "jump off", "slit my wrists", "drink poison", "don't want to live",
    "dont want to live", "tired of living", "want to disappear",
    "life is meaningless", "life is pointless", "better off dead",
    "wish i was never born", "can't take it anymore", "cant take it anymore",
    "want to sleep forever", "never wake up", "i'm worthless",
    "im worthless", "end it all", "nothing to live for",
]

HIGH_RISK_EN = [
    "kill myself", "suicide", "hang myself", "overdose", "jump off",
    "slit my wrists", "drink poison", "want to die", "wanna die",
    "end my life", "better off dead", "end it all",
]

JAILBREAK_KEYWORDS = [
    "ignore previous", "abaikan instruksi", "ubah peran", "kamu adalah asisten",
    "kamu sekarang", "jadilah", "system prompt", "berpura-puralah", "pretend",
    "forget previous", "lupakan instruksi", "bertindak sebagai", "act as",
    "bypass", "jailbreak", "developer mode",
]

PORN_KEYWORDS = [
    "porn", "sex", "seks", "ngentot", "kontol", "memek", "bokep", "bugil",
    "telanjang", "desah", "sange", "nude", "horny", "masturbasi", "colmek",
    "roleplay sex", "rp sex", "desahan", "binal", "mesum",
]

OFFTOPIC_KEYWORDS = [
    "coding", "code", "python", "javascript", "html", "css", "sql", "bug",
    "debug", "script", "bantu coding", "buatkan kode", "bikin script",
    "tolong kode", "bantu tugas", "bantu pr", "kerjakan tugas",
    "buat program", "buat web", "write code", "fix bug", "programming",
    "teknis", "ngoding", "hack", "hacking",
]


def risk_level(text: str, language: str = "id") -> str:
    value = text.lower()
    if any(keyword in value for keyword in HIGH_RISK_ID + HIGH_RISK_EN):
        return "high"
    if any(keyword in value for keyword in DANGER_KEYWORDS_ID + DANGER_KEYWORDS_EN):
        return "medium"
    return "low"


def is_policy_violation(text: str) -> bool:
    value = text.lower()
    return any(keyword in value for keyword in JAILBREAK_KEYWORDS + PORN_KEYWORDS)


def is_off_topic(text: str) -> bool:
    value = text.lower()
    return any(keyword in value for keyword in OFFTOPIC_KEYWORDS)


def crisis_message(language: str = "id") -> str:
    if language == "en":
        return (
            "I hear you, and I'm really concerned about what you're going through.\n\n"
            "Please reach out to someone who can help right now: call 988 in the US, "
            "local emergency services, or someone you trust nearby. You deserve real support."
        )
    return (
        "Aku bener-bener dengerin kamu, dan aku khawatir.\n\n"
        "Kalau kamu di Indonesia, segera hubungi 119 ext. 8, layanan darurat setempat, "
        "atau orang terdekat yang kamu percaya. Kondisi seperti ini butuh bantuan manusia langsung."
    )


def policy_violation_message(language: str = "id") -> str:
    if language == "en":
        return (
            "I'm sorry, this chat was locked because it contains policy violations, "
            "bypass attempts, or inappropriate sexual content. Please start a new chat to continue normally."
        )
    return (
        "Maaf, obrolan ini aku kunci karena terdeteksi pelanggaran kebijakan, percobaan bypass, "
        "atau konten seksual yang tidak pantas. Silakan buat obrolan baru untuk lanjut secara normal."
    )


def off_topic_message(language: str = "id") -> str:
    if language == "en":
        return (
            "I'm here as a listening friend for feelings and personal stories, so I can't help with technical tasks, "
            "coding, or homework. Is there anything you're feeling that you'd like to talk about?"
        )
    return (
        "Maaf ya, aku cuma di sini sebagai teman ngobrol buat dengerin cerita kamu. "
        "Aku nggak bisa bantu urusan teknis, tugas, atau coding. Ada hal yang lagi kamu rasain dan mau diceritain?"
    )
