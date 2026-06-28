from .state import clamp

BOND_LEVELS = ("stranger", "familiar", "trusted", "friend", "beloved menace")

CARE_COMMANDS = ("feed", "play", "pet", "clean", "sleep", "wake")
_COUNT_ATTR = {command: f"{command}_count" for command in CARE_COMMANDS}

TRUST_GAIN = {"feed": 3, "play": 2, "pet": 4, "clean": 3, "sleep": 1, "wake": 1, "nickname": 1}
CRITICAL_BONUS = 6


def is_critical(pet):
    return pet.hunger >= 85 or pet.health <= 20 or pet.cleanliness <= 15 or pet.energy <= 10


def bond_for(trust_score):
    if trust_score >= 80:
        return "beloved menace"
    if trust_score >= 55:
        return "friend"
    if trust_score >= 30:
        return "trusted"
    if trust_score >= 12:
        return "familiar"
    return "stranger"


def record(user, command, pet, was_critical=False):
    user.total_interactions += 1

    attr = _COUNT_ATTR.get(command)
    if attr:
        setattr(user, attr, getattr(user, attr) + 1)

    gain = TRUST_GAIN.get(command, 0)
    if attr and was_critical:
        gain += CRITICAL_BONUS
    if gain:
        user.trust_score = clamp(user.trust_score + gain, 0, 100)

    user.bond_level = bond_for(user.trust_score)
