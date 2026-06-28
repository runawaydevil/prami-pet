from datetime import timedelta

from prami import engine, milestones
from prami.models import utcnow


def test_first_interaction_awarded(session, pet, user):
    user.total_interactions = 1
    achieved = milestones.check(session, pet, user, "status", False)
    assert any(m["key"] == "first_interaction" for m in achieved)


def test_milestone_not_repeated(session, pet, user):
    user.total_interactions = 1
    milestones.check(session, pet, user, "status", False)
    again = milestones.check(session, pet, user, "status", False)
    assert all(m["key"] != "first_interaction" for m in again)


def test_critical_save_is_favourite_worthy(session, pet, user):
    user.total_interactions = 5
    achieved = milestones.check(session, pet, user, "feed", was_critical=True)
    save = [m for m in achieved if m["key"] == "first_critical_save"]
    assert save and save[0]["favourite"] is True


def test_bond_milestone(session, pet, user):
    user.total_interactions = 5
    user.bond_level = "friend"
    achieved = milestones.check(session, pet, user, "pet", False)
    assert any(m["key"] == "reached_friend" for m in achieved)


def test_first_feeding_via_engine(session, pet, user, config):
    pet.hunger = 50
    result = engine.handle(session, pet, user, "feed", config)
    keys = {m["key"] for m in result.milestones}
    assert "first_feeding" in keys


def test_seven_days_alive(session, pet, user, config):
    pet.born_at = utcnow() - timedelta(days=8)
    result = engine.handle(session, pet, user, "status", config)
    assert any(m["key"] == "7_days_alive" for m in result.milestones)


def test_major_milestone_is_boost_eligible(session, pet, user):
    user.total_interactions = 5
    # force the all-time interaction count past 100 by seeding interactions
    from prami import repository as repo
    for i in range(101):
        repo.record_interaction(session, pet.id, user.id, "pet", None, True)
    achieved = milestones.check(session, pet, user, "pet", False)
    hundred = [m for m in achieved if m["key"] == "100_interactions"]
    assert hundred and hundred[0]["boost"] is True
