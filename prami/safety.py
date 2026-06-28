from datetime import timedelta

from . import repository as repo
from .models import utcnow
from .sanitize import clean_nickname

PRIVATE_VISIBILITIES = ("private", "direct")


def may_reply(settings, user):
    return not settings.paused and not user.blocked


def may_autopost(settings):
    return settings.autopost_enabled and not settings.paused


def may_use_nickname(nickname):
    return clean_nickname(nickname) is not None


def may_store_memory(config):
    return config.enable_teach_command


def may_favourite(session, settings, config, user, visibility, status_id, now=None):
    now = now or utcnow()
    if not settings.favourites_enabled or settings.paused:
        return False, "favourites disabled"
    if user is None or user.blocked:
        return False, "blocked user"
    if visibility in PRIVATE_VISIBILITIES and not config.allow_favourite_private:
        return False, "private status"
    if repo.has_social_action(session, status_id, "favourite"):
        return False, "already favourited"
    if repo.count_social_actions(session, "favourite", now - timedelta(hours=1)) >= config.max_favourites_per_hour:
        return False, "hourly cap reached"
    if repo.count_social_actions(session, "favourite", now - timedelta(days=1), user.id) >= config.max_favourites_per_user_per_day:
        return False, "per-user daily cap reached"
    return True, "ok"


def may_boost(session, settings, config, user, visibility, status_id, now=None):
    now = now or utcnow()
    if not settings.boosts_enabled or settings.paused:
        return False, "boosts disabled"
    if user is None or user.blocked:
        return False, "blocked user"
    if visibility in PRIVATE_VISIBILITIES:
        return False, "private status"
    if config.boost_only_public_statuses and visibility != "public":
        return False, "not a public status"
    if repo.has_social_action(session, status_id, "boost"):
        return False, "already boosted"
    if repo.count_social_actions(session, "boost", now - timedelta(days=1)) >= config.max_boosts_per_day:
        return False, "daily boost cap reached"
    last = repo.last_social_action_at(session, "boost")
    if last and now - last < timedelta(hours=config.min_hours_between_boosts):
        return False, "too soon since last boost"
    return True, "ok"
