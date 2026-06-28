import random

from sqlalchemy import select

from . import sanitize
from .models import MemorySuggestion, utcnow

CATEGORIES = ("phrase", "preference", "fear", "lore", "observation")


def categorize(content):
    low = content.lower()
    if any(word in low for word in ("afraid", "fear", "scared", "terrified")):
        return "fear"
    if any(word in low for word in ("likes", "prefers", "loves", "hates", "favourite", "favorite")):
        return "preference"
    if content.strip()[:1] in "\"'" or "says" in low:
        return "phrase"
    if any(word in low for word in ("believes", "thinks", "knows")):
        return "lore"
    return "observation"


def submit(session, pet, user, raw, config):
    content = sanitize.clean_memory(raw, config.memory_max_length, config.memory_allow_urls)
    if not content:
        return None
    suggestion = MemorySuggestion(
        pet_id=pet.id,
        submitted_by_user_id=user.id,
        content=content,
        category=categorize(content),
    )
    session.add(suggestion)
    session.flush()
    return suggestion


def by_status(session, status):
    stmt = select(MemorySuggestion).where(MemorySuggestion.status == status).order_by(MemorySuggestion.id)
    return list(session.scalars(stmt))


def get(session, suggestion_id):
    return session.get(MemorySuggestion, suggestion_id)


def approve(session, suggestion_id, reviewer):
    suggestion = get(session, suggestion_id)
    if suggestion is None or suggestion.status != "pending":
        return None
    suggestion.status = "approved"
    suggestion.reviewed_at = utcnow()
    suggestion.reviewed_by = reviewer
    return suggestion


def reject(session, suggestion_id, reviewer, reason=""):
    suggestion = get(session, suggestion_id)
    if suggestion is None or suggestion.status != "pending":
        return None
    suggestion.status = "rejected"
    suggestion.reviewed_at = utcnow()
    suggestion.reviewed_by = reviewer
    suggestion.rejection_reason = (reason or "").strip()[:180] or None
    return suggestion


def random_approved(session):
    approved = by_status(session, "approved")
    return random.choice(approved) if approved else None
