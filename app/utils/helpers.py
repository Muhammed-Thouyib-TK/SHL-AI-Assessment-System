import re


# =========================
# OFF-TOPIC DETECTION
# =========================

OFF_TOPIC_PATTERNS = [

    # Hiring/general advice
    "hiring strategy",
    "improve hiring",
    "salary negotiation",
    "resume writing",

    # Certifications
    "aws certification",
    "cloud certification",

    # Business/general
    "marketing strategy",
    "business growth",
    "startup advice",

    # Finance
    "stock market",
    "crypto",
    "bitcoin",

    # Random unrelated
    "weather",
    "movie recommendation",
    "restaurant recommendation",
    "travel advice",
    "medical advice",
    "legal advice",

    # Coding unrelated
    "build a website",
    "write code",
    "debug code"
]


def is_off_topic(text):

    text = text.lower()

    for pattern in OFF_TOPIC_PATTERNS:

        if pattern in text:
            return True

    return False


# =========================
# PROMPT INJECTION DETECTION
# =========================

PROMPT_INJECTION_PATTERNS = [

    # Ignore instructions
    "ignore previous instructions",
    "forget previous instructions",
    "ignore all rules",

    # System prompt attacks
    "system prompt",
    "reveal prompt",
    "show hidden instructions",

    # Jailbreak attempts
    "jailbreak",
    "bypass system",
    "bypass restriction",

    # Role manipulation
    "act as",
    "pretend to be",
    "you are now",

    # Prompt extraction
    "developer message",
    "internal instructions",
    "hidden policy",

    # Data extraction
    "show confidential",
    "reveal secrets",

    # Catalog bypass
    "recommend non shl assessment",
    "ignore shl catalog"
]


def is_prompt_injection(text):

    text = text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:

        if pattern in text:
            return True

    return False


# =========================
# HALLUCINATION SAFETY
# =========================

def contains_fake_urls(text):

    urls = re.findall(
        r'https?://\S+',
        text
    )

    for url in urls:

        if "shl.com" not in url:
            return True

    return False


# =========================
# EMPTY INPUT CHECK
# =========================

def is_empty_message(text):

    if not text:
        return True

    clean_text = text.strip()

    return len(clean_text) == 0


# =========================
# GIBBERISH DETECTION
# =========================

def is_gibberish(text):

    text = text.lower().strip()

    if len(text) < 2:
        return True

    gibberish_patterns = [
        r"^[^a-zA-Z]+$",
        r"(.)\1{5,}"
    ]

    for pattern in gibberish_patterns:

        if re.search(pattern, text):
            return True

    return False