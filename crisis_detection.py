from config import CRISIS_KEYWORDS

def detect_crisis(text):
    text_lower = text.lower()
    for word in CRISIS_KEYWORDS:
        if word in text_lower:
            return True
    return False