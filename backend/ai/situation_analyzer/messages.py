"""Localised strings (en / ur / sd) used by the analyzer and SMS alerts."""

LANGS = ("en", "ur", "sd")

CATEGORY = {
    "en": {"assault": "Physical assault / violence", "stalking": "Stalking / being followed", "harassment": "Harassment",
           "medical": "Medical emergency", "accident": "Accident / fire", "distress": "Call for help", "other": "Unclear situation"},
    "ur": {"assault": "حملہ / تشدد", "stalking": "پیچھا کیا جانا", "harassment": "ہراسانی",
           "medical": "طبی ایمرجنسی", "accident": "حادثہ / آگ", "distress": "مدد کی پکار", "other": "غیر واضح صورتحال"},
    "sd": {"assault": "حملو / تشدد", "stalking": "پٺيان لڳڻ", "harassment": "هراسگي",
           "medical": "طبي ايمرجنسي", "accident": "حادثو / باهه", "distress": "مدد جي پڪار", "other": "اڻڄاتل صورتحال"},
}
LEVEL = {
    "en": {"low": "Low", "medium": "Medium", "high": "High", "critical": "Critical"},
    "ur": {"low": "کم", "medium": "درمیانہ", "high": "زیادہ", "critical": "انتہائی"},
    "sd": {"low": "گهٽ", "medium": "وچولو", "high": "وڌيڪ", "critical": "انتهائي"},
}
SUMMARY = {
    "en": "{category} detected. Threat level: {level} ({score}/100).",
    "ur": "{category} کا پتہ چلا۔ خطرے کی سطح: {level} ({score}/100)۔",
    "sd": "{category} جو پتو پيو. خطري جي سطح: {level} ({score}/100).",
}
SUMMARY_CALM = {
    "en": "No emergency detected.",
    "ur": "کسی ایمرجنسی کا پتہ نہیں چلا۔",
    "sd": "ڪابه ايمرجنسي نه ملي.",
}
ACTIONS = {
    "en": {
        "calm": "Stay calm and move toward a well-lit, crowded place.",
        "alerting": "Your trusted contacts are being alerted with your live location.",
        "emergency": "Call emergency services now (Police 15 / Rescue 1122).",
        "stalking": "Do not go straight home. Head to a shop, crowd or police station.",
        "harassment": "If safe, record evidence and note the time and place.",
    },
    "ur": {
        "calm": "پرسکون رہیں اور کسی روشن، پرہجوم جگہ کی طرف جائیں۔",
        "alerting": "آپ کے قابلِ اعتماد رابطوں کو آپ کی لائیو لوکیشن کے ساتھ الرٹ بھیجا جا رہا ہے۔",
        "emergency": "فوراً ایمرجنسی سروس کو کال کریں (پولیس 15 / ریسکیو 1122)۔",
        "stalking": "سیدھے گھر نہ جائیں۔ کسی دکان، ہجوم یا تھانے کی طرف جائیں۔",
        "harassment": "اگر محفوظ ہو تو ثبوت محفوظ کریں اور وقت اور جگہ نوٹ کریں۔",
    },
    "sd": {
        "calm": "پرسڪون رهو ۽ روشن، ماڻهن واري هنڌ ڏانهن وڃو.",
        "alerting": "توهان جي ڀروسي وارن رابطن کي توهان جي لائيو هنڌ سان الرٽ موڪليو پيو وڃي.",
        "emergency": "فوري ايمرجنسي سروس کي ڪال ڪريو (پوليس 15 / ريسڪيو 1122).",
        "stalking": "سڌو گهر نه وڃو. ڪنهن دڪان، ميڙ يا ٿاڻي ڏانهن وڃو.",
        "harassment": "جيڪڏهن محفوظ هجي ته ثبوت محفوظ ڪريو ۽ وقت ۽ هنڌ نوٽ ڪريو.",
    },
}
SMS_SOS = {
    "en": "🚨 SOS from {name}! Situation: {category}. Threat level: {level}. Live location: {link}",
    "ur": "🚨 {name} کی طرف سے ایمرجنسی الرٹ! صورتحال: {category}۔ خطرے کی سطح: {level}۔ لائیو لوکیشن: {link}",
    "sd": "🚨 {name} طرفان ايمرجنسي الرٽ! صورتحال: {category}. خطري جي سطح: {level}. لائيو هنڌ: {link}",
}
SMS_SAFE = {
    "en": "✅ {name} has marked themselves safe. Thank you for being there.",
    "ur": "✅ {name} نے بتایا ہے کہ اب وہ محفوظ ہیں۔ آپ کا شکریہ۔",
    "sd": "✅ {name} ٻڌايو آهي ته هاڻي هوءَ محفوظ آهي. توهان جي مهرباني.",
}


def pick(table: dict, lang: str):
    return table.get(lang if lang in LANGS else "en")
