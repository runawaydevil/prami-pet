from datetime import timedelta

from prami import engine, events
from prami.models import utcnow


def make_event(session, pet, config, key="egg"):
    template = next(t for t in events.TEMPLATES if t["key"] == key)
    return events.start(session, pet, config, template=template)


def test_start_creates_active_event(session, pet, config):
    event = make_event(session, pet, config)
    assert event.status == "active"
    assert events.active(session).id == event.id


def test_only_one_active_event(session, pet, config):
    make_event(session, pet, config)
    assert events.maybe_start(session, pet, config, force=True) is None


def test_vote_one_per_user(session, pet, user, config):
    event = make_event(session, pet, config)
    ok, _ = events.vote(session, event, user, "hatch")
    assert ok is True
    again, reason = events.vote(session, event, user, "guard")
    assert again is False and reason == "already voted"


def test_vote_unknown_option(session, pet, user, config):
    event = make_event(session, pet, config)
    ok, reason = events.vote(session, event, user, "banana")
    assert ok is False and reason == "unknown option"


def test_complete_applies_winning_outcome(session, pet, user, config):
    event = make_event(session, pet, config, key="snack_vote")
    pet.hunger = 80
    events.vote(session, event, user, "soup")
    outcome = events.complete(session, event, pet)
    assert event.status == "completed"
    assert pet.hunger == 60
    assert "Soup" in outcome


def test_complete_without_votes_uses_first_option(session, pet, config):
    event = make_event(session, pet, config, key="egg")
    assert events.complete(session, event, pet)
    assert event.status == "completed"


def test_expire_due_completes_past_events(session, pet, config):
    event = make_event(session, pet, config)
    event.ends_at = utcnow() - timedelta(hours=1)
    done = events.expire_due(session, pet)
    assert len(done) == 1
    assert event.status == "completed"


def test_engine_vote_flow(session, pet, user, config):
    make_event(session, pet, config, key="snack_vote")
    result = engine.handle(session, pet, user, "vote", config, arg="soup")
    assert result.accepted is True


def test_engine_event_show_when_none(session, pet, user, config):
    result = engine.handle(session, pet, user, "event", config)
    assert result.text
