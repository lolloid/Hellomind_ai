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
        return "medium"
    return "low"


def check_risk(text: str) -> bool:
    """Return True jika terdeteksi ada indikasi bahaya."""
    return risk_level(text) in ("high", "medium")


CRISIS_MESSAGE = (
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
