from prami import engine
from prami.relationships import bond_for, is_critical, record


def test_bond_levels_by_trust():
    assert bond_for(0) == "stranger"
    assert bond_for(11) == "stranger"
    assert bond_for(12) == "familiar"
    assert bond_for(30) == "trusted"
    assert bond_for(55) == "friend"
    assert bond_for(80) == "beloved menace"


def test_record_counts_and_trust(pet, user):
    record(user, "pet", pet)
    assert user.total_interactions == 1
    assert user.pet_count == 1
    assert user.trust_score == 4
    assert user.bond_level == "stranger"


def test_bond_progresses_with_care(pet, user):
    for _ in range(3):
        record(user, "pet", pet)
    assert user.trust_score == 12
    assert user.bond_level == "familiar"


def test_non_care_command_counts_but_no_per_command_field(pet, user):
    record(user, "status", pet)
    assert user.total_interactions == 1
    assert user.feed_count == 0
    assert user.trust_score == 0


def test_critical_save_grants_bonus(pet, user):
    record(user, "feed", pet, was_critical=True)
    assert user.trust_score == 9


def test_is_critical_detects_bad_states(pet):
    pet.hunger, pet.health, pet.cleanliness, pet.energy = 90, 90, 70, 70
    assert is_critical(pet) is True
    pet.hunger = 40
    assert is_critical(pet) is False


def test_engine_records_relationship(session, pet, user, config):
    engine.handle(session, pet, user, "feed", config)
    assert user.feed_count == 1
    assert user.total_interactions == 1
    assert user.trust_score >= 3
