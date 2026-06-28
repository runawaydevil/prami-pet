from prami import engine, memory
from prami import repository as repo


def as_admin(config, user):
    config.admin_accounts = [user.acct]


def test_nonadmin_is_ignored(session, pet, user, config):
    config.admin_accounts = []
    assert engine.handle(session, pet, user, "admin", config, arg="pause") is None


def test_nonadmin_refusal_when_configured(session, pet, user, config):
    config.admin_accounts = []
    config.admin_refuse_nonadmin = True
    result = engine.handle(session, pet, user, "admin", config, arg="pause")
    assert result is not None and result.accepted is False


def test_admin_pause_and_resume(session, pet, user, config):
    as_admin(config, user)
    engine.handle(session, pet, user, "admin", config, arg="pause")
    assert repo.get_settings(session, config).paused is True
    engine.handle(session, pet, user, "admin", config, arg="resume")
    assert repo.get_settings(session, config).paused is False


def test_admin_pause_blocks_other_users(session, pet, user, config):
    as_admin(config, user)
    engine.handle(session, pet, user, "admin", config, arg="pause")
    other = repo.get_or_create_user(session, "bob@example.social")
    assert engine.handle(session, pet, other, "feed", config) is None


def test_admin_toggle_favourites(session, pet, user, config):
    as_admin(config, user)
    engine.handle(session, pet, user, "admin", config, arg="set-favourites on")
    assert repo.get_settings(session, config).favourites_enabled is True


def test_admin_set_visibility(session, pet, user, config):
    as_admin(config, user)
    engine.handle(session, pet, user, "admin", config, arg="set-visibility public")
    assert repo.get_settings(session, config).default_visibility == "public"


def test_admin_approve_memory(session, pet, user, config):
    as_admin(config, user)
    config.enable_teach_command = True
    other = repo.get_or_create_user(session, "carol@example.social")
    suggestion = memory.submit(session, pet, other, "Prami likes blankets", config)
    result = engine.handle(session, pet, user, "admin", config, arg=f"approve-memory {suggestion.id}")
    assert "Approved" in result.text
    assert memory.get(session, suggestion.id).status == "approved"


def test_admin_block_and_unblock(session, pet, user, config):
    as_admin(config, user)
    engine.handle(session, pet, user, "admin", config, arg="block @troll@bad.social")
    assert repo.get_user(session, "troll@bad.social").blocked is True
    engine.handle(session, pet, user, "admin", config, arg="unblock @troll@bad.social")
    assert repo.get_user(session, "troll@bad.social").blocked is False


def test_admin_status_text(session, pet, user, config):
    as_admin(config, user)
    result = engine.handle(session, pet, user, "admin", config, arg="status")
    assert "paused=" in result.text
