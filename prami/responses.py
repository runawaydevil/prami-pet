import random

from . import personality as personality_mod
from . import templates
from .config import config

# Back-compatible names; the data lives in templates.py.
TEMPLATES = templates.COMMAND_TEMPLATES
AUTOPOST = templates.AUTOPOST

PACKS = {"default": (templates.COMMAND_TEMPLATES, templates.AUTOPOST)}


def _pack():
    return PACKS.get(config.personality_pack, PACKS["default"])


def _personality(pet):
    text = getattr(pet, "personality", None) or config.pet_personality
    return personality_mod.from_string(text)


def _render(pool, pet):
    line = random.choice(pool)
    return line.format(name=pet.name) if "{" in line else line


def variant_for(command, pet):
    p = _personality(pet)
    if command == "feed":
        if pet.hunger >= 75:
            return "very_hungry"
        if pet.hunger <= 12:
            return "already_full"
        if pet.chaos >= p.chaos_threshold:
            return "chaotic"
        if pet.trust <= p.suspicion_threshold:
            return "suspicious"
        if pet.happiness >= p.happy_threshold:
            return "happy"
        return "normal"

    if command == "play":
        if pet.energy <= p.tired_threshold:
            return "tired"
        if pet.chaos >= p.chaos_threshold:
            return "chaotic"
        if pet.happiness >= p.happy_threshold or pet.energy >= 75:
            return "energetic"
        return "normal"

    if command == "pet":
        if pet.asleep:
            return "asleep"
        if pet.trust <= p.suspicion_threshold:
            return "low_trust"
        if pet.happiness < 30 or pet.chaos >= p.chaos_threshold:
            return "annoyed"
        if pet.trust >= 70:
            return "high_trust"
        if pet.happiness >= p.happy_threshold:
            return "affectionate"
        return "normal"

    if command == "clean":
        if pet.cleanliness >= 85:
            return "already_clean"
        if pet.chaos >= p.chaos_threshold:
            return "chaotic"
        if pet.cleanliness <= 30:
            return "dirty"
        return "normal" if pet.trust >= 60 else "angry"

    if command == "sleep":
        if pet.energy >= 80:
            return "too_energetic"
        if pet.energy <= 30:
            return "grateful"
        return "normal"

    if command == "wake":
        if pet.energy < 20:
            return "too_tired"
        if pet.chaos >= p.chaos_threshold or pet.happiness < 35:
            return "annoyed"
        return "normal"

    return "normal"


def _status_variant(pet, p):
    if pet.asleep:
        return "asleep"
    if pet.hunger >= 75:
        return "hungry"
    if pet.health < 30 or pet.happiness < 30:
        return "sad"
    if pet.energy <= 25:
        return "tired"
    if pet.chaos >= p.chaos_threshold:
        return "chaotic"
    if pet.cleanliness <= 30:
        return "dirty"
    if pet.happiness >= p.happy_threshold:
        return "happy"
    return "normal"


def for_command(command, pet):
    groups = _pack()[0][command]
    variant = variant_for(command, pet)
    return _render(groups.get(variant) or groups["normal"], pet)


def status(pet):
    groups = _pack()[0]["status"]
    variant = _status_variant(pet, _personality(pet))
    return _render(groups.get(variant) or groups["normal"], pet)


def already_asleep(pet):
    return _render(_pack()[0]["sleep"]["already_asleep"], pet)


def already_awake(pet):
    return _render(_pack()[0]["wake"]["already_awake"], pet)


def too_sleepy(command, pet):
    groups = _pack()[0].get(command, {})
    return _render(groups.get("asleep") or templates.ASLEEP_REJECTION, pet)


def cooldown(command, reason, pet):
    return _render(templates.COOLDOWN.get(reason, templates.COOLDOWN["global"]), pet)


def too_much(pet):
    return _render(templates.TOO_MUCH, pet)


def unknown(pet):
    return _render(templates.UNKNOWN, pet)


def nickname_set(pet, nick):
    return random.choice(templates.NICKNAME_SET).format(name=pet.name, nick=nick)


def nickname_cleared(pet):
    return _render(templates.NICKNAME_CLEARED, pet)


def nickname_rejected(pet):
    return _render(templates.NICKNAME_REJECTED, pet)


def teach_ack(pet):
    return _render(templates.TEACH_ACK, pet)


def teach_disabled(pet):
    return _render(templates.TEACH_DISABLED, pet)


def teach_rejected(pet):
    return _render(templates.TEACH_REJECTED, pet)


def no_event(pet):
    return _render(templates.NO_EVENT, pet)


def event_show(pet, title, description, options):
    return templates.EVENT_SHOW.format(name=pet.name, title=title, description=description, options=options)


def event_help(pet, title, options):
    return templates.EVENT_HELP.format(name=pet.name, title=title, options=options)


def vote_ack(pet, title):
    return random.choice(templates.VOTE_ACK).format(name=pet.name, title=title)


def vote_rejected(pet, reason, options):
    if reason == "already voted":
        return templates.VOTE_REJECTED_ALREADY.format(name=pet.name)
    return templates.VOTE_REJECTED_UNKNOWN.format(name=pet.name, options=options)


def maybe_address(text, user):
    nick = getattr(user, "nickname", None)
    if not nick:
        return text
    warm = getattr(user, "bond_level", "stranger") in ("friend", "beloved menace")
    if random.random() < (0.3 if warm else 0.15):
        return f"{nick}, {text}"
    return text


def autopost_group(pet):
    p = _personality(pet)
    if pet.asleep:
        return "sleepy"
    if pet.hunger >= 70:
        return "hungry"
    if pet.energy <= 25:
        return "sleepy"
    if pet.chaos >= p.chaos_threshold:
        return "chaotic"
    if pet.cleanliness <= 30:
        return "dirty"
    if pet.social <= 25:
        return "lonely"
    if pet.happiness >= p.happy_threshold:
        return "happy"
    return "weird_observation"


def autopost(pet):
    posts = _pack()[1]
    group = autopost_group(pet)
    flavor = ("weird_observation", "existential", "community_appreciation")
    keys = [group] * 4 + list(flavor)
    return _render(posts[random.choice(keys)], pet)


def help_text(config):
    return templates.HELP_TEXT.format(name=config.pet_name, species=config.pet_species)
