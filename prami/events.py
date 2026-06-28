import json
import random
from datetime import timedelta

from sqlalchemy import func, select

from .models import CommunityEvent, EventVote, utcnow
from .state import clamp
from .templates import EVENT_SCENARIOS as TEMPLATES


def active(session, now=None):
    return session.scalars(
        select(CommunityEvent).where(CommunityEvent.status == "active").order_by(CommunityEvent.id)
    ).first()


def options_text(event):
    return ", ".join(f"{key} ({opt['label']})" for key, opt in json.loads(event.options).items())


def _active_count(session):
    return session.scalar(
        select(func.count()).select_from(CommunityEvent).where(CommunityEvent.status == "active")
    ) or 0


def _last_event_end(session):
    return session.scalar(
        select(func.max(CommunityEvent.ends_at)).where(CommunityEvent.status.in_(("completed", "expired")))
    )


def start(session, pet, config, now=None, template=None):
    now = now or utcnow()
    tmpl = template or random.choice(TEMPLATES)
    event = CommunityEvent(
        pet_id=pet.id,
        key=tmpl["key"],
        title=tmpl["title"],
        description=tmpl["description"],
        options=json.dumps(tmpl["options"]),
        status="active",
        starts_at=now,
        ends_at=now + timedelta(hours=config.event_duration_hours),
    )
    session.add(event)
    session.flush()
    return event


def maybe_start(session, pet, config, now=None, force=False):
    now = now or utcnow()
    if active(session, now) or _active_count(session) >= config.max_active_events:
        return None
    if not force:
        last_end = _last_event_end(session)
        if last_end and now - last_end < timedelta(hours=config.event_cooldown_hours):
            return None
        if random.random() >= config.event_chance_per_autopost:
            return None
    return start(session, pet, config, now)


def vote(session, event, user, option):
    options = json.loads(event.options)
    option = (option or "").strip().lower()
    if option not in options:
        return False, "unknown option"
    existing = session.scalars(
        select(EventVote).where(EventVote.event_id == event.id, EventVote.user_id == user.id)
    ).first()
    if existing:
        return False, "already voted"
    session.add(EventVote(event_id=event.id, user_id=user.id, option=option))
    session.flush()
    return True, "ok"


def complete(session, event, pet, now=None):
    options = json.loads(event.options)
    tally = {}
    for v in session.scalars(select(EventVote).where(EventVote.event_id == event.id)):
        tally[v.option] = tally.get(v.option, 0) + 1

    order = list(options)
    if tally:
        winner = max(tally, key=lambda key: (tally[key], -order.index(key)))
    else:
        winner = order[0]

    outcome = options[winner]
    for stat, delta in outcome.get("deltas", {}).items():
        setattr(pet, stat, clamp(getattr(pet, stat) + delta))

    event.status = "completed"
    event.outcome = outcome["text"]
    return outcome["text"]


def expire_due(session, pet, now=None):
    now = now or utcnow()
    due = session.scalars(
        select(CommunityEvent).where(CommunityEvent.status == "active", CommunityEvent.ends_at <= now)
    )
    return [complete(session, event, pet, now) for event in list(due)]
