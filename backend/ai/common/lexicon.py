"""Multilingual emergency lexicon: English, Urdu, Sindhi (Arabic script) and Roman Urdu/Sindhi.

Text and lexicon terms go through the SAME normalisation, so spelling variants of Urdu/Sindhi
letters (ي/ی, ك/ک, ڪ/ک, ڇ/چ ...) still match each other.
"""
import re
import unicodedata
from typing import Dict, List

# ---------- normalisation ----------
_MAP = {
    # Arabic/Persian/Urdu variants -> one form
    "ي": "ی", "ى": "ی", "ې": "ی", "ئ": "ی", "ۓ": "ی", "ے": "ی",
    "ك": "ک", "ڪ": "ک",
    "ہ": "ه", "ۃ": "ه", "ة": "ه", "ۂ": "ه",
    "أ": "ا", "إ": "ا", "آ": "ا", "ٲ": "ا",
    "ؤ": "و", "ۆ": "و",
    "ں": "ن", "ڻ": "ن", "ڱ": "ن", "ڃ": "ن",
    "ٹ": "ت", "ٿ": "ت", "ٽ": "ت", "ٺ": "ت",
    "ڈ": "د", "ڏ": "د", "ڊ": "د", "ڌ": "د", "ڍ": "د", "ݙ": "د",
    "ڑ": "ر", "ڙ": "ر",
    "ڇ": "چ", "ڄ": "ج", "ڳ": "گ", "ڀ": "ب", "ٻ": "ب", "ڦ": "ف", "ڇ": "چ",
    "ھ": "",           # aspiration marker
    "ء": "", "ٔ": "",
    "\u200c": " ", "\u200d": "", "\u0640": "",   # ZWNJ, ZWJ, tatweel
}
_TABLE = str.maketrans(_MAP)
_ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F]")
_SINDHI_CHARS = set("ڪڳڱڻٿٽڏڊڌڍڇڄڙڀٻڦڃݙ")
_SINDHI_WORDS = {"آهي", "آهيان", "کي", "جو", "جي", "ڪري", "رهيو", "رهي", "مون", "توهان", "نه", "ڏيو", "ڪريو"}


def normalize(text: str) -> str:
    t = unicodedata.normalize("NFKC", text or "").lower()
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")   # strip diacritics
    t = t.translate(_TABLE)
    t = re.sub(r"[^\w\s']", " ", t, flags=re.UNICODE)                 # punctuation -> space
    t = re.sub(r"([a-z])\1{2,}", r"\1", t)                            # helppp -> help, bachaooo -> bachao
    return re.sub(r"\s+", " ", t).strip()


def detect_language(text: str) -> str:
    """Return 'sd', 'ur', 'roman' (Roman Urdu/Sindhi) or 'en' (heuristic)."""
    raw = text or ""
    if _ARABIC_RE.search(raw):
        if any(ch in _SINDHI_CHARS for ch in raw):
            return "sd"
        words = set(raw.split())
        return "sd" if len(words & _SINDHI_WORDS) >= 2 else "ur"
    low = normalize(raw)
    if any(re.search(r"\b" + re.escape(w) + r"\b", low) for w in ROMAN_MARKERS):
        return "roman"
    return "en"


ROMAN_MARKERS = ["mujhe", "mujhy", "mera", "meri", "mukhe", "bachao", "bachayo", "madad", "karo", "kar", "raha", "rahi",
                 "hai", "nahi", "nahin", "koi", "aahe", "chor", "chhor", "peecha", "pecha"]

# ---------- lexicon ----------
# category -> list of terms (all languages together). Latin terms use whole-word matching,
# Arabic-script terms use prefix matching (so inflections like بچاؤں still match).
RAW: Dict[str, List[str]] = {
    "distress": [
        # English
        "help", "help me", "somebody help", "save me", "leave me alone", "let me go", "get away", "stop it",
        "please no", "call the police", "no no", "don't touch me", "dont touch me",
        # Urdu
        "بچاؤ", "مجھے بچاؤ", "مدد", "مدد کرو", "میری مدد کرو", "چھوڑ دو", "مجھے چھوڑ دو", "چھوڑو", "دور رہو",
        "پولیس کو بلاؤ", "کوئی ہے", "خدا کے لیے", "اللہ کے لیے", "نہیں نہیں", "مجھے جانے دو", "ہٹو",
        # Sindhi
        "بچايو", "مون کي بچايو", "مدد ڪريو", "منهنجي مدد ڪريو", "ڇڏي ڏيو", "مون کي ڇڏيو", "پري ٿيو",
        "پوليس کي سڏيو", "ڪو آهي", "الله لاءِ", "نه نه", "مون کي وڃڻ ڏيو",
        # Roman Urdu / Sindhi
        "bachao", "bachaao", "mujhe bachao", "mujhy bachao", "bachayo", "mukhe bachayo", "madad", "madad karo",
        "meri madad karo", "madad kryo", "madad kio", "chhor do", "chor do", "chhod do", "mujhe chor do",
        "mujhe chhor do", "chadyo", "mukhe chadyo", "door raho", "dur raho", "police bulao", "police ko bulao",
        "police ko saddyo", "koi hai", "koi aahe", "khuda ke liye", "allah ke liye", "nahi nahi", "nahin nahin",
        "jaane do", "mujhe jane do", "hato",
    ],
    "assault": [
        "attack", "attacked", "hit me", "hitting me", "beating me", "beat me", "rape", "raped", "assault", "knife", "gun",
        "weapon", "kidnap", "kidnapped", "grabbed me", "choking", "strangle", "he is hurting me",
        "حملہ", "مار رہا", "مار رہی", "مجھے مار", "مارو", "چاقو", "چھری", "بندوق", "پستول", "اغوا", "زبردستی",
        "گھسیٹ", "ریپ", "زیادتی", "پکڑ لیا", "گلا دبا",
        "حملو", "ماري رهيو", "مون کي ماري", "ماريو", "ڇري", "زوري", "ڇڪي", "ريپ", "زيادتي", "پڪڙيو", "ڌڪ",
        "hamla", "maar raha", "maar rahi", "mujhe maar", "maar do", "maaro", "chaku", "chhuri", "bandook", "pistol",
        "agwa", "zabardasti", "zabar dasti", "ghaseet", "pakar liya", "pakad liya", "zulm",
    ],
    "stalking": [
        "following me", "follows me", "followed me", "is following", "stalker", "stalking", "behind me",
        "watching me", "chasing me", "someone follows",
        "پیچھا کر", "میرا پیچھا", "میرے پیچھے", "تعاقب", "نظر رکھ", "گاڑی میرے پیچھے",
        "پٺيان", "پٺيان پيو", "منهنجي پٺيان", "تعاقب ڪري", "نظر رکي",
        "peecha kar", "pecha kar", "picha kar", "pichha kar", "mera peecha", "mere peeche", "mere pichhe",
        "tafaqub", "pathian pyo", "pathyan pyo", "peeche pyo", "pichhy",
    ],
    "harassment": [
        "harass", "harassing", "harassment", "touching me", "touched me", "catcall", "eve teasing", "molest",
        "inappropriate", "threatening me", "threat", "abusing me", "don't touch",
        "تنگ کر", "ہراساں", "ہراسان", "چھیڑ", "چھو رہا", "ہاتھ مت لگاؤ", "ہاتھ نہ لگاؤ", "ہاتھ لگا", "دھمکی",
        "بدتمیزی", "گندی نظر", "گندے کمنٹ",
        "تنگ ڪري", "هراسان", "ڇيڙ", "ڇهي رهيو", "هٿ نه لڳايو", "ڌمڪي", "بدتميزي",
        "tang kar", "tang kr", "harasaan", "chher", "chheda", "chhoo raha", "chhu raha", "haath mat lagao",
        "hath mat lagao", "hath na lagao", "haath na lagao", "dhamki", "dhamkiyan", "badtameezi", "gandi nazar",
        "hath na lagayo",
    ],
    "medical": [
        "bleeding", "faint", "fainted", "unconscious", "chest pain", "heart attack", "can't breathe", "cannot breathe",
        "cant breathe", "seizure", "injured", "ambulance", "not breathing",
        "خون", "بے ہوش", "سانس نہیں", "دل کا درد", "سینے میں درد", "چوٹ", "زخمی", "دورہ", "ایمبولینس",
        "رت وهي", "بيهوش", "ساهه نٿو", "ساه", "ڇاتي ۾ درد", "دل جو درد", "ايمبولينس",
        "khoon", "behosh", "saans nahi", "saans nahin", "dil ka dard", "seene mein dard", "chot", "zakhmi",
        "daura", "saah nathi",
    ],
    "accident": [
        "accident", "crash", "collision", "on fire", "fire", "fell down", "trapped",
        "حادثہ", "ایکسیڈنٹ", "آگ لگ", "پھنس گئ", "ٹکر", "گاڑی ٹکرا",
        "حادثو", "ايڪسيڊنٽ", "باهه لڳي", "ڦاٿل", "ٽڪر",
        "hadsa", "hadsah", "aag lag", "phans gai", "phas gayi", "takkar", "gaari takra",
    ],
    "danger": [
        "scared", "afraid", "danger", "dangerous", "unsafe", "alone", "dark", "drunk", "lost", "frightened",
        "ڈر لگ", "خوف", "خطرہ", "اکیلی", "اکیلا", "اندھیرا", "غیر محفوظ", "گھبرا",
        "ڊڄان", "ڊپ", "خطرو", "اڪيلي", "اڪيلو", "انڌيرو", "غير محفوظ",
        "dar lag", "dar lagta", "darr", "khauf", "khatra", "akeli", "akela", "andhera", "ghabra", "ghair mehfooz",
    ],
}


def _compile():
    out = {}
    for cat, terms in RAW.items():
        pats = []
        for term in terms:
            n = normalize(term)
            if not n:
                continue
            latin = bool(re.fullmatch(r"[a-z0-9' ]+", n))
            core = re.escape(n)
            pat = (r"\b" + core + r"\b") if latin else (r"(?<!\w)" + core)
            pats.append((n, re.compile(pat)))
        out[cat] = pats
    return out


_COMPILED = _compile()


def find_matches(text: str) -> Dict[str, Dict[str, int]]:
    """Return {category: {term: occurrences}} for every lexicon hit in `text`."""
    t = normalize(text)
    result: Dict[str, Dict[str, int]] = {}
    for cat, pats in _COMPILED.items():
        hits = {}
        for term, rx in pats:
            n = len(rx.findall(t))
            if n:
                hits[term] = n
        # drop terms fully contained in a longer matched term (e.g. "help" inside "help me")
        for a in list(hits):
            if any(a != b and a in b for b in hits):
                hits.pop(a)
        if hits:
            result[cat] = hits
    return result
