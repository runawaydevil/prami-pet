from datetime import timedelta

from sqlalchemy import func, select, text

from . import events, memory
from . import repository as repo
from .models import Event, Interaction, User, utcnow


def collect(session, config, settings, now=None):
    now = now or utcnow()
    pet = repo.get_pet(session)
    day_ago = now - timedelta(hours=24)

    last_startup = session.scalar(select(func.max(Event.created_at)).where(Event.kind == "startup"))

    interactions_24h = session.scalar(
        select(func.count()).select_from(Interaction).where(
            Interaction.accepted.is_(True), Interaction.created_at >= day_ago
        )
    ) or 0
    unique_users_24h = session.scalar(
        select(func.count(func.distinct(Interaction.user_id))).where(
            Interaction.accepted.is_(True), Interaction.created_at >= day_ago
        )
    ) or 0
    autoposts_24h = session.scalar(
        select(func.count()).select_from(Event).where(Event.kind == "autopost", Event.created_at >= day_ago)
    ) or 0
    blocked = session.scalar(select(func.count()).select_from(User).where(User.blocked.is_(True))) or 0

    top = session.execute(
        select(Interaction.command, func.count().label("n"))
        .where(Interaction.accepted.is_(True))
        .group_by(Interaction.command)
        .order_by(func.count().desc())
        .limit(5)
    ).all()

    active = events.active(session, now)

    return {
        "uptime_seconds": (now - last_startup).total_seconds() if last_startup else None,
        "total_interactions": repo.count_interactions_total(session),
        "interactions_24h": interactions_24h,
        "unique_users_24h": unique_users_24h,
        "mood": pet.mood,
        "critical_stats": _critical_stats(pet),
        "key_stats": {
            "hunger": pet.hunger, "energy": pet.energy, "health": pet.health,
            "cleanliness": pet.cleanliness, "social": pet.social,
        },
        "autoposts_24h": autoposts_24h,
        "favourites_24h": repo.count_social_actions(session, "favourite", day_ago),
        "boosts_24h": repo.count_social_actions(session, "boost", day_ago),
        "active_event": active.title if active else None,
        "pending_memories": len(memory.by_status(session, "pending")),
        "blocked_users": blocked,
        "top_commands": [(row[0], row[1]) for row in top],
        "last_decay_at": pet.last_decay_at,
        "last_autopost_at": pet.last_autopost_at,
        "last_autopost_category": pet.last_autopost_category,
        "database": _database_status(session, config),
    }


def _critical_stats(pet):
    breaches = []
    if pet.hunger >= 85:
        breaches.append(f"hunger {pet.hunger}")
    if pet.health <= 20:
        breaches.append(f"health {pet.health}")
    if pet.cleanliness <= 15:
        breaches.append(f"cleanliness {pet.cleanliness}")
    if pet.energy <= 10:
        breaches.append(f"energy {pet.energy}")
    return breaches


def _database_status(session, config):
    try:
        session.execute(text("SELECT 1"))
        dialect = config.database_url.split("://", 1)[0].split("+")[0] or "unknown"
        return f"connected ({dialect})"
    except Exception as exc:
        return f"error: {exc}"


def _fmt_dt(value):
    return f"{value:%Y-%m-%d %H:%M} UTC" if value else "never"


def _fmt_uptime(seconds):
    if seconds is None:
        return "—"
    total = int(seconds)
    days, total = divmod(total, 86400)
    hours, total = divmod(total, 3600)
    minutes = total // 60
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours or days:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


def render(data):
    keys = data["key_stats"]
    critical = ", ".join(data["critical_stats"]) or "none"
    top = ", ".join(f"{cmd}:{n}" for cmd, n in data["top_commands"]) or "none"
    last_post = _fmt_dt(data["last_autopost_at"])
    if data["last_autopost_category"]:
        last_post += f" ({data['last_autopost_category']})"

    return "\n".join([
        "Prami — local stats",
        f"uptime: {_fmt_uptime(data['uptime_seconds'])}",
        f"mood: {data['mood']} · critical: {critical}",
        f"stats: hunger={keys['hunger']} energy={keys['energy']} health={keys['health']} "
        f"clean={keys['cleanliness']} social={keys['social']}",
        f"interactions: {data['total_interactions']} total · {data['interactions_24h']} in 24h · "
        f"{data['unique_users_24h']} unique users 24h",
        f"top commands: {top}",
        f"autoposts 24h: {data['autoposts_24h']} · favourites 24h: {data['favourites_24h']} · "
        f"boosts 24h: {data['boosts_24h']}",
        f"active event: {data['active_event'] or 'none'}",
        f"pending memories: {data['pending_memories']} · blocked users: {data['blocked_users']}",
        f"last decay: {_fmt_dt(data['last_decay_at'])}",
        f"last autopost: {last_post}",
        f"database: {data['database']}",
    ])


def text_report(session, config, settings, now=None):
    return render(collect(session, config, settings, now))
