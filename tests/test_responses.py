import pytest

from prami import responses


def set_state(pet, **kwargs):
    for key, value in kwargs.items():
        setattr(pet, key, value)
    return pet


def test_every_template_pool_is_non_empty():
    for command, groups in responses.TEMPLATES.items():
        assert "normal" in groups, f"{command} is missing a normal variant"
        for variant, pool in groups.items():
            assert pool, f"{command}/{variant} is empty"
    for group, pool in responses.AUTOPOST.items():
        assert pool, f"autopost/{group} is empty"


@pytest.mark.parametrize(
    "command,state,expected",
    [
        ("feed", {"hunger": 90}, "very_hungry"),
        ("feed", {"hunger": 5}, "already_full"),
        ("feed", {"hunger": 40, "trust": 5}, "suspicious"),
        ("play", {"energy": 8}, "tired"),
        ("play", {"energy": 85, "happiness": 50}, "energetic"),
        ("pet", {"trust": 5}, "low_trust"),
        ("pet", {"trust": 85, "happiness": 50, "chaos": 10}, "high_trust"),
        ("clean", {"cleanliness": 95}, "already_clean"),
        ("clean", {"cleanliness": 10, "chaos": 10}, "dirty"),
        ("sleep", {"energy": 90}, "too_energetic"),
        ("sleep", {"energy": 15}, "grateful"),
        ("wake", {"energy": 10}, "too_tired"),
    ],
)
def test_variant_selection_matches_state(pet, command, state, expected):
    set_state(pet, **state)
    assert responses.variant_for(command, pet) == expected


def test_personality_shifts_chaotic_threshold(pet):
    set_state(pet, hunger=40, trust=40, happiness=50, chaos=58)

    pet.personality = "calm and gentle"
    assert responses.variant_for("feed", pet) == "normal"

    pet.personality = "chaotic, weird"
    assert responses.variant_for("feed", pet) == "chaotic"


def test_responses_actually_vary(pet):
    set_state(pet, hunger=40, energy=70, happiness=50, chaos=10, trust=40)
    seen = {responses.for_command("feed", pet) for _ in range(40)}
    assert len(seen) > 1


def test_response_stays_short(pet):
    for _ in range(30):
        line = responses.for_command("feed", pet)
        assert line.count(".") <= 4
        assert len(line) < 300


@pytest.mark.parametrize(
    "state",
    [
        {"asleep": True},
        {"hunger": 90},
        {"energy": 10},
        {"happiness": 95, "energy": 70},
        {"happiness": 10},
        {"chaos": 95},
        {"cleanliness": 5},
        {},
    ],
)
def test_status_handles_all_states(pet, state):
    set_state(pet, **state)
    line = responses.status(pet)
    assert line
    assert pet.name in line


def test_pet_name_is_applied(pet):
    pet.name = "Glorbo"
    assert "Glorbo" in responses.status(pet)


@pytest.mark.parametrize(
    "state,expected",
    [
        ({"hunger": 90}, "hungry"),
        ({"asleep": True}, "sleepy"),
        ({"social": 10, "hunger": 40, "energy": 70, "chaos": 10, "cleanliness": 70}, "lonely"),
        ({"cleanliness": 10, "hunger": 40, "energy": 70, "chaos": 10, "social": 60}, "dirty"),
        ({"chaos": 95, "hunger": 40, "energy": 70}, "chaotic"),
    ],
)
def test_autopost_group_reflects_state(pet, state, expected):
    set_state(pet, **state)
    assert responses.autopost_group(pet) == expected


def test_autopost_returns_varied_lines(pet):
    set_state(pet, hunger=40, energy=70, happiness=50, social=60, chaos=10, cleanliness=70)
    seen = {responses.autopost(pet) for _ in range(60)}
    assert len(seen) > 1


def test_asleep_rejection_and_no_op_responses(pet):
    pet.asleep = True
    assert responses.too_sleepy("feed", pet)
    assert responses.already_asleep(pet)
    assert responses.already_awake(pet)
