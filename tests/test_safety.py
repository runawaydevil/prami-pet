from prami import repository as repo
from prami import safety


def settings_with(session, config, **overrides):
    settings = repo.get_settings(session, config)
    for key, value in overrides.items():
        setattr(settings, key, value)
    return settings


def test_favourites_disabled_by_default(session, pet, user, config):
    settings = repo.get_settings(session, config)
    allowed, _ = safety.may_favourite(session, settings, config, user, "public", "1")
    assert allowed is False


def test_favourite_allowed_when_enabled(session, pet, user, config):
    settings = settings_with(session, config, favourites_enabled=True)
    allowed, why = safety.may_favourite(session, settings, config, user, "public", "1")
    assert allowed is True
    assert why == "ok"


def test_favourite_rejects_blocked_user(session, pet, user, config):
    settings = settings_with(session, config, favourites_enabled=True)
    user.blocked = True
    allowed, _ = safety.may_favourite(session, settings, config, user, "public", "1")
    assert allowed is False


def test_favourite_rejects_private_by_default(session, pet, user, config):
    settings = settings_with(session, config, favourites_enabled=True)
    allowed, _ = safety.may_favourite(session, settings, config, user, "direct", "1")
    assert allowed is False


def test_favourite_allows_private_when_configured(session, pet, user, config):
    config.allow_favourite_private = True
    settings = settings_with(session, config, favourites_enabled=True)
    allowed, _ = safety.may_favourite(session, settings, config, user, "private", "1")
    assert allowed is True


def test_favourite_no_duplicate(session, pet, user, config):
    settings = settings_with(session, config, favourites_enabled=True)
    repo.record_social_action(session, pet.id, user.id, "9", "favourite")
    allowed, why = safety.may_favourite(session, settings, config, user, "public", "9")
    assert allowed is False
    assert "already" in why


def test_favourite_hourly_cap(session, pet, user, config):
    config.max_favourites_per_hour = 1
    settings = settings_with(session, config, favourites_enabled=True)
    repo.record_social_action(session, pet.id, user.id, "1", "favourite")
    allowed, _ = safety.may_favourite(session, settings, config, user, "public", "2")
    assert allowed is False


def test_boosts_disabled_by_default(session, pet, user, config):
    settings = repo.get_settings(session, config)
    allowed, _ = safety.may_boost(session, settings, config, user, "public", "1")
    assert allowed is False


def test_boost_only_public(session, pet, user, config):
    settings = settings_with(session, config, boosts_enabled=True)
    allowed, _ = safety.may_boost(session, settings, config, user, "unlisted", "1")
    assert allowed is False


def test_boost_allowed_for_public_when_enabled(session, pet, user, config):
    settings = settings_with(session, config, boosts_enabled=True)
    allowed, why = safety.may_boost(session, settings, config, user, "public", "1")
    assert allowed is True


def test_boost_respects_min_interval(session, pet, user, config):
    config.max_boosts_per_day = 5
    settings = settings_with(session, config, boosts_enabled=True)
    repo.record_social_action(session, pet.id, user.id, "1", "boost")
    allowed, why = safety.may_boost(session, settings, config, user, "public", "2")
    assert allowed is False


def test_paused_blocks_favourites(session, pet, user, config):
    settings = settings_with(session, config, favourites_enabled=True, paused=True)
    allowed, _ = safety.may_favourite(session, settings, config, user, "public", "1")
    assert allowed is False
