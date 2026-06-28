from datetime import timedelta

from prami import engine, responses, sanitize
from prami.models import utcnow


def test_clean_nickname_valid():
    assert sanitize.clean_nickname("Soup Wizard") == "Soup Wizard"


def test_clean_nickname_truncates_to_32():
    assert len(sanitize.clean_nickname("x" * 50)) == 32


def test_clean_nickname_rejects_urls():
    assert sanitize.clean_nickname("see http://evil.example") is None
    assert sanitize.clean_nickname("www.evil.example") is None


def test_clean_nickname_rejects_mentions():
    assert sanitize.clean_nickname("hi @bob@server.social") is None


def test_clean_nickname_strips_html():
    assert sanitize.clean_nickname("<b>Soup</b>") == "Soup"


def test_clean_nickname_collapses_breaks():
    assert sanitize.clean_nickname("Soup\n\n  Wizard") == "Soup Wizard"


def test_clean_nickname_empty_is_none():
    assert sanitize.clean_nickname("   ") is None


def test_nickname_set_then_clear(session, pet, user, config):
    result = engine.handle(session, pet, user, "nickname", config, arg="Soup Wizard")
    assert result.accepted is True
    assert user.nickname == "Soup Wizard"

    later = utcnow() + timedelta(minutes=6)
    engine.handle(session, pet, user, "nickname", config, arg="clear", now=later)
    assert user.nickname is None


def test_nickname_invalid_is_rejected(session, pet, user, config):
    result = engine.handle(session, pet, user, "nickname", config, arg="http://x.example")
    assert result.accepted is False
    assert user.nickname is None


def test_nickname_cooldown_blocks_quick_second(session, pet, user, config):
    engine.handle(session, pet, user, "nickname", config, arg="One")
    second = engine.handle(session, pet, user, "nickname", config, arg="Two")
    assert second.accepted is False
    assert user.nickname == "One"


class _FakeUser:
    def __init__(self, nickname, bond_level="stranger"):
        self.nickname = nickname
        self.bond_level = bond_level


def test_maybe_address_can_use_nickname():
    u = _FakeUser("Soup", "friend")
    used = any(responses.maybe_address("Prami did a thing.", u).startswith("Soup, ") for _ in range(200))
    assert used


def test_maybe_address_without_nickname_is_unchanged():
    u = _FakeUser(None)
    assert responses.maybe_address("hello", u) == "hello"
