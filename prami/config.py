import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _int(name, default):
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return int(raw)


def _bool(name, default):
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _float(name, default):
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return float(raw)


def _csv(name):
    raw = os.getenv(name, "")
    return [item.strip().lstrip("@") for item in raw.split(",") if item.strip()]


@dataclass
class Config:
    mastodon_base_url: str = os.getenv("MASTODON_BASE_URL", "")
    mastodon_access_token: str = os.getenv("MASTODON_ACCESS_TOKEN", "")
    bot_acct: str = os.getenv("BOT_ACCOUNT_ACCT", "").lstrip("@")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///prami.db")

    poll_interval: int = _int("POLL_INTERVAL_SECONDS", 30)
    decay_interval: int = _int("STATE_DECAY_INTERVAL_MINUTES", 15)
    autopost_interval: int = _int("AUTOPOST_INTERVAL_MINUTES", 240)

    default_visibility: str = os.getenv("DEFAULT_VISIBILITY", "unlisted")
    autopost_visibility: str = os.getenv("AUTOPOST_VISIBILITY", "unlisted")
    autopost_enabled: bool = _bool("AUTOPOST_ENABLED", True)

    pet_name: str = os.getenv("PET_NAME", "Prami")
    pet_species: str = os.getenv("PET_SPECIES", "community critter")
    pet_personality: str = os.getenv("PET_PERSONALITY", "weird, affectionate, slightly dramatic")
    personality_pack: str = os.getenv("PET_PERSONALITY_PACK", "default")

    max_per_user_hour: int = _int("MAX_COMMANDS_PER_USER_PER_HOUR", 20)
    max_global_hour: int = _int("MAX_COMMANDS_GLOBAL_PER_HOUR", 200)
    blocked_users: list = field(default_factory=lambda: _csv("BLOCKED_USERS"))

    processed_retention_days: int = _int("PROCESSED_RETENTION_DAYS", 14)

    enable_favourites: bool = _bool("ENABLE_FAVOURITES", False)
    max_favourites_per_hour: int = _int("MAX_FAVOURITES_PER_HOUR", 8)
    max_favourites_per_user_per_day: int = _int("MAX_FAVOURITES_PER_USER_PER_DAY", 3)
    allow_favourite_private: bool = _bool("ALLOW_FAVOURITE_PRIVATE", False)

    enable_boosts: bool = _bool("ENABLE_BOOSTS", False)
    max_boosts_per_day: int = _int("MAX_BOOSTS_PER_DAY", 1)
    min_hours_between_boosts: int = _int("MIN_HOURS_BETWEEN_BOOSTS", 12)
    boost_only_public_statuses: bool = _bool("BOOST_ONLY_PUBLIC_STATUSES", True)

    enable_teach_command: bool = _bool("ENABLE_TEACH_COMMAND", False)
    admin_accounts: list = field(default_factory=lambda: _csv("ADMIN_ACCOUNTS"))
    admin_refuse_nonadmin: bool = _bool("ADMIN_REFUSE_NONADMIN", False)
    memory_allow_urls: bool = _bool("MEMORY_ALLOW_URLS", False)
    memory_max_length: int = _int("MEMORY_MAX_LENGTH", 180)

    enable_events: bool = _bool("ENABLE_EVENTS", False)
    event_chance_per_autopost: float = _float("EVENT_CHANCE_PER_AUTOPOST", 0.15)
    max_active_events: int = _int("MAX_ACTIVE_EVENTS", 1)
    event_duration_hours: int = _int("EVENT_DURATION_HOURS", 12)
    event_cooldown_hours: int = _int("EVENT_COOLDOWN_HOURS", 24)

    enable_milestone_posts: bool = _bool("ENABLE_MILESTONE_POSTS", True)
    milestone_post_visibility: str = os.getenv("MILESTONE_POST_VISIBILITY", "unlisted")

    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def is_admin(self, acct):
        target = (acct or "").lstrip("@").lower()
        return any(target == a.lower() for a in self.admin_accounts)


config = Config()
