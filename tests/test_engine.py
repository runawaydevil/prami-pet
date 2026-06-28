from datetime import timedelta

from prami import engine
from prami import repository as repo
from prami.models import utcnow
from prami.state import compute_mood


def test_feed_reduces_hunger_and_is_accepted(session, pet, user, config):
    pet.hunger = 80
    result = engine.handle(session, pet, user, "feed", config)
    assert result.accepted is True
    assert pet.hunger == 45


def test_stats_never_leave_bounds(session, pet, user, config):
    pet.hunger = 10
    engine.handle(session, pet, user, "feed", config)
    assert pet.hunger == 0
    assert 0 <= pet.happiness <= 100


def test_overfeeding_raises_chaos(session, pet, user, config):
    pet.hunger = 20
    pet.chaos = 30
    engine.handle(session, pet, user, "feed", config)
    assert pet.chaos > 30


def test_play_drops_energy_and_raises_chaos(session, pet, user, config):
    pet.energy = 80
    pet.chaos = 20
    engine.handle(session, pet, user, "play", config)
    assert pet.energy == 65
    assert pet.chaos == 25


def test_clean_costs_some_happiness(session, pet, user, config):
    pet.cleanliness = 20
    pet.happiness = 60
    engine.handle(session, pet, user, "clean", config)
    assert pet.cleanliness == 60
    assert pet.happiness == 54


def test_user_cooldown_blocks_second_feed(session, pet, user, config):
    first = engine.handle(session, pet, user, "feed", config)
    second = engine.handle(session, pet, user, "feed", config)
    assert first.accepted is True
    assert second.accepted is False


def test_cooldown_clears_after_window(session, pet, user, config):
    now = utcnow()
    engine.handle(session, pet, user, "feed", config, now=now)
    again = engine.handle(session, pet, user, "feed", config, now=now + timedelta(minutes=31))
    assert again.accepted is True


def test_global_per_command_rate_limit(session, pet, user, config):
    now = utcnow()
    for i in range(5):
        other = repo.get_or_create_user(session, f"u{i}@example.social")
        result = engine.handle(session, pet, other, "clean", config, now=now)
        assert result.accepted is True
    blocked = repo.get_or_create_user(session, "late@example.social")
    sixth = engine.handle(session, pet, blocked, "clean", config, now=now)
    assert sixth.accepted is False


def test_sleep_then_wake_toggles_state(session, pet, user, config):
    engine.handle(session, pet, user, "sleep", config)
    assert pet.asleep is True
    engine.handle(session, pet, user, "wake", config)
    assert pet.asleep is False


def test_sleep_global_cooldown_applies_across_users(session, pet, user, config):
    now = utcnow()
    engine.handle(session, pet, user, "sleep", config, now=now)
    engine.handle(session, pet, user, "wake", config, now=now)
    other = repo.get_or_create_user(session, "second@example.social")
    blocked = engine.handle(session, pet, other, "sleep", config, now=now + timedelta(minutes=1))
    assert blocked.accepted is False


def test_active_care_rejected_while_asleep(session, pet, user, config):
    pet.asleep = True
    result = engine.handle(session, pet, user, "play", config)
    assert result.accepted is False
    assert pet.asleep is True


def test_blocked_user_is_silently_ignored(session, pet, user, config):
    user.blocked = True
    assert engine.handle(session, pet, user, "feed", config) is None


def test_per_user_hourly_cap(session, pet, user, config):
    config.max_per_user_hour = 1
    engine.handle(session, pet, user, "status", config)
    capped = engine.handle(session, pet, user, "status", config)
    assert capped.accepted is False


def test_unknown_command_still_responds(session, pet, user, config):
    result = engine.handle(session, pet, user, None, config)
    assert result is not None
    assert result.accepted is True


def test_mood_reflects_hunger(session, pet):
    pet.hunger = 90
    pet.asleep = False
    assert compute_mood(pet) == "ravenous"
