import pytest

from prami import cli, engine, memory
from prami import repository as repo
from prami.actions.registry import REGISTRY, build_registry
from prami.config import Config, config as app_config
from prami.db import session_scope
from prami.parser import parse


# --- Registry: alias resolution -------------------------------------------------

def test_aliases_resolve_to_canonical_names():
    assert REGISTRY.canonical("food") == "feed"
    assert REGISTRY.canonical("pat") == "pet"
    assert REGISTRY.canonical("nick") == "nickname"
    assert REGISTRY.canonical("?") == "help"
    assert REGISTRY.canonical("unmapped") is None


def test_phrase_aliases_resolve():
    phrases = REGISTRY.phrase_map()
    assert phrases.get("call me") == "nickname"
    assert phrases.get("name me") == "nickname"


def test_resolve_falls_back_to_unknown():
    assert REGISTRY.resolve("feed").name == "feed"
    assert REGISTRY.resolve("zzz").name == "unknown"


def test_a_fresh_registry_has_every_command():
    registry = build_registry()
    for name in ("status", "feed", "play", "pet", "clean", "sleep", "wake",
                 "nickname", "teach", "event", "vote", "admin", "help"):
        assert name in registry.names()


# --- Disabled commands ----------------------------------------------------------

def test_teach_is_config_gated():
    cfg = Config()
    cfg.enable_teach_command = False
    assert REGISTRY.is_enabled("teach", cfg) is False
    cfg.enable_teach_command = True
    assert REGISTRY.is_enabled("teach", cfg) is True


def test_disabled_command_does_not_execute(session, pet, user, config):
    config.enable_teach_command = False
    result = engine.handle(session, pet, user, "teach", config, arg="Prami fears printers")
    assert result.accepted is False
    assert memory.by_status(session, "pending") == []


# --- Admin-only actions ---------------------------------------------------------

def test_admin_action_is_admin_only():
    assert REGISTRY.resolve("admin").admin_only is True
    assert REGISTRY.resolve("feed").admin_only is False


def test_nonadmin_cannot_run_admin_action(session, pet, user, config):
    config.admin_accounts = []
    assert engine.handle(session, pet, user, "admin", config, arg="pause") is None


def test_admin_action_runs_for_admin(session, pet, user, config):
    config.admin_accounts = [user.acct]
    result = engine.handle(session, pet, user, "admin", config, arg="status")
    assert result is not None and "paused=" in result.text


# --- CLI and Mastodon share the same core path ----------------------------------

def test_parsed_alias_resolves_to_same_action():
    parsed = parse("<p>@prami food</p>")
    assert REGISTRY.resolve(parsed.name) is REGISTRY.resolve("feed")


def test_engine_dispatches_through_registry(session, pet, user, config, monkeypatch):
    seen = []
    original = REGISTRY.resolve
    monkeypatch.setattr(REGISTRY, "resolve", lambda name: seen.append(name) or original(name))
    engine.handle(session, pet, user, "feed", config)
    assert "feed" in seen


@pytest.fixture
def cli_db(tmp_path, monkeypatch):
    monkeypatch.setattr(app_config, "database_url", f"sqlite:///{tmp_path / 'cli.db'}")
    cli.main(["reset", "--yes"])


def test_cli_runs_through_engine_handle(cli_db, monkeypatch):
    seen = []
    original = engine.handle
    monkeypatch.setattr(engine, "handle", lambda *a, **k: seen.append(a[3]) or original(*a, **k))
    cli.main(["feed", "--user", "@alice@example.com"])
    assert "feed" in seen


def test_cli_and_mastodon_paths_reach_same_state(cli_db):
    cli.main(["feed", "--user", "@cli@x.com"])
    with session_scope() as s:
        cli_hunger = repo.get_pet(s).hunger

    cli.main(["reset", "--yes"])
    parsed = parse("<p>@prami food</p>")  # what the Mastodon poller feeds the engine
    with session_scope() as s:
        pet = repo.get_pet(s)
        user = repo.get_or_create_user(s, "masto@x.com")
        engine.handle(s, pet, user, parsed.name, app_config, arg=parsed.arg)
        masto_hunger = pet.hunger

    assert cli_hunger == masto_hunger == 5
