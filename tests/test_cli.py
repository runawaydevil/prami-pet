import pytest

from prami import cli
from prami import repository as repo
from prami.config import config
from prami.db import session_scope


@pytest.fixture
def cli_db(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "database_url", f"sqlite:///{tmp_path / 'cli.db'}")
    cli.main(["reset", "--yes"])


def current_pet():
    with session_scope() as session:
        pet = repo.get_pet(session)
        session.expunge(pet)
        return pet


def test_feed_changes_state_through_cli(cli_db, capsys):
    cli.main(["feed", "--user", "@alice@example.com"])
    out = capsys.readouterr().out.strip()
    assert out
    assert current_pet().hunger == 5


def test_status_is_narrative_not_raw_numbers(cli_db, capsys):
    cli.main(["status", "--user", "@alice@example.com"])
    out = capsys.readouterr().out
    assert "Prami" in out
    assert "hunger :" not in out


def test_debug_state_exposes_raw_numbers(cli_db, capsys):
    cli.main(["debug-state"])
    out = capsys.readouterr().out
    for field in ("hunger", "happiness", "energy", "health", "cleanliness", "social", "trust", "chaos", "asleep", "mood", "updated_at"):
        assert field in out


def test_feed_cooldown_blocks_second_call(cli_db, capsys):
    cli.main(["feed", "--user", "@alice@example.com"])
    cli.main(["feed", "--user", "@alice@example.com"])
    assert current_pet().hunger == 5


def test_different_users_are_independent(cli_db):
    cli.main(["feed", "--user", "@alice@example.com"])
    cli.main(["feed", "--user", "@bob@example.com"])
    assert current_pet().hunger == 0


def test_tick_applies_decay(cli_db):
    before = current_pet().hunger
    cli.main(["tick"])
    assert current_pet().hunger > before


def test_tick_hours_scales_with_decay_interval(cli_db):
    cli.main(["tick", "--hours", "3"])
    assert current_pet().hunger == 100


def test_sleep_and_wake_toggle_state(cli_db):
    cli.main(["sleep", "--user", "@alice@example.com"])
    assert current_pet().asleep is True
    cli.main(["wake", "--user", "@alice@example.com"])
    assert current_pet().asleep is False


def test_reset_restores_defaults(cli_db):
    cli.main(["feed", "--user", "@alice@example.com"])
    cli.main(["reset", "--yes"])
    assert current_pet().hunger == 40


def test_cli_nickname_sets_and_appears_in_relationship(cli_db, capsys):
    cli.main(["nickname", "Soup", "Wizard", "--user", "@alice@example.com"])
    capsys.readouterr()
    cli.main(["relationship", "--user", "@alice@example.com"])
    out = capsys.readouterr().out
    assert "Soup Wizard" in out
    assert "bond_level" in out


def test_cli_relationship_tracks_interaction_counts(cli_db, capsys):
    cli.main(["feed", "--user", "@alice@example.com"])
    cli.main(["pet", "--user", "@alice@example.com"])
    capsys.readouterr()
    cli.main(["relationship", "--user", "@alice@example.com"])
    out = capsys.readouterr().out
    assert "total_interactions" in out
    assert "trust_score" in out


def test_blocked_user_gets_no_response(cli_db, capsys):
    monkey_block(["alice@example.com"])
    cli.main(["feed", "--user", "@alice@example.com"])
    out = capsys.readouterr().out
    assert "blocked" in out.lower()


def monkey_block(accts):
    with session_scope() as session:
        for acct in accts:
            repo.block_user(session, acct)
