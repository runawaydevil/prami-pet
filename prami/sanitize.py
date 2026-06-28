import re

_TAG = re.compile(r"<[^>]+>")
_URL = re.compile(r"https?://|www\.", re.IGNORECASE)
_WHITESPACE = re.compile(r"\s+")

NICKNAME_MAX = 32


def clean_nickname(raw):
    if not raw:
        return None
    text = _WHITESPACE.sub(" ", _TAG.sub("", raw)).strip()
    if not text:
        return None
    if "@" in text or _URL.search(text):
        return None
    return text[:NICKNAME_MAX]


def clean_memory(raw, max_len=180, allow_urls=False):
    if not raw:
        return None
    text = _WHITESPACE.sub(" ", _TAG.sub("", raw)).strip()
    if len(text) >= 2 and text[0] in "\"'" and text[-1] == text[0]:
        text = text[1:-1].strip()
    if not text or "@" in text:
        return None
    if not allow_urls and _URL.search(text):
        return None
    return text[:max_len]
