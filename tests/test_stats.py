from datetime import timedelta

from prami import decay, engine, events, memory, stats
from prami import repository as repo
from prami.models import utcnow


def _collect(session, config):
    return stats.collect(session, config, repo.get_settings(session, config), utcnow())


def test_counts_interactions_and_unique_users(session, pet, config):
    a = repo.get_or_create_user(session, "a@x.com")
    b = repo.get_or_create_user(session, "b@x.com")
    repo.record_interaction(session, pet.id, a.id, "feed", None, True)
    repo.record_interaction(session, pet.id, b.id, "pet", None, True)
    repo.record_interaction(session, pet.id, a.id, "feed", None, True)

    data = _collect(session, config)
    assert data["total_interactions"] == 3
    assert data["interactions_24h"] == 3
    assert data["unique_users_24h"] == 2
    assert ("feed", 2) in data["top_commands"]


def test_social_memory_and_blocked_counts(session, pet, user, config):
    repo.record_social_action(session, pet.id, user.id, "1", "favourite")
    repo.record_social_action(session, pet.id, user.id, "2", "boost")
    config.enable_teach_command = True
    memory.submit(session, pet, user, "Prami likes soup", config)
    repo.block_user(session, "troll@bad.social")

    data = _collect(session, config)
    assert data["favourites_24h"] == 1
    assert data["boosts_24h"] == 1
    assert data["pending_memories"] == 1
    assert data["blocked_users"] == 1


def test_active_event_and_mood(session, pet, config):
    pet.mood = "ravenous"
    template = next(t for t in events.TEMPLATES if t["key"] == "egg")
    events.start(session, pet, config, template=template)

    data = _collect(session, config)
    assert data["active_event"] == "Prami found a mysterious egg."
    assert data["mood"] == "ravenous"


def test_critical_stats_are_listed(session, pet, config):
    pet.hunger = 95
    pet.energy = 5
    data = _collect(session, config)
    assert any("hunger" in entry for entry in data["critical_stats"])
    assert any("energy" in entry for entry in data["critical_stats"])


def test_uptime_is_none_without_startup(session, pet, config):
    assert _collect(session, config)["uptime_seconds"] is None


def test_uptime_from_startup_event(session, pet, config):
    repo.log_event(session, pet.id, "startup", "started")
    session.flush()
    data = stats.collect(session, config, repo.get_settings(session, config), utcnow() + timedelta(hours=2))
    assert data["uptime_seconds"] >= 7000


def test_last_decay_tracked(session, pet, config):
    assert _collect(session, config)["last_decay_at"] is None
    decay.tick(pet)
    assert _collect(session, config)["last_decay_at"] is not None


def test_database_status_connected(session, pet, config):
    assert "connected" in _collect(session, config)["database"]


def test_render_is_readable(session, pet, config):
    report = stats.text_report(session, config, repo.get_settings(session, config), utcnow())
    for label in ("uptime", "mood", "interactions", "database", "active event"):
        assert label in report


def test_admin_stats_command(session, pet, user, config):
    config.admin_accounts = [user.acct]
    result = engine.handle(session, pet, user, "admin", config, arg="stats")
    assert result is not None
    assert "uptime" in result.text and "database" in result.text


def test_stats_not_available_to_non_admin(session, pet, user, config):
    config.admin_accounts = []
    assert engine.handle(session, pet, user, "admin", config, arg="stats") is None
