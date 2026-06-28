from .. import relationships, responses, social
from ..state import clamp, compute_mood
from .base import Action, Outcome


def _snapshot(pet):
    return {
        "hunger": pet.hunger,
        "social": pet.social,
        "cleanliness": pet.cleanliness,
        "health": pet.health,
        "energy": pet.energy,
        "chaos": pet.chaos,
    }


class CareAction(Action):
    def effect(self, pet):
        raise NotImplementedError

    def run(self, ctx):
        pet = ctx.pet
        text = responses.for_command(self.name, pet)
        before = _snapshot(pet)
        before_critical = relationships.is_critical(pet)

        self.effect(pet)
        pet.mood = compute_mood(pet)

        return Outcome(
            text=text,
            favourite=social.favourite_worthy(self.name, before, ctx.user),
            boost=social.boost_worthy(before_critical, relationships.is_critical(pet)),
            was_critical=before_critical,
        )


class FeedAction(CareAction):
    name = "feed"
    aliases = ("food", "eat", "snack", "feast")
    runs_while_asleep = False
    user_cooldown_minutes = 30
    per_hour_limit = 10

    def effect(self, pet):
        was_hungry = pet.hunger > 60
        pet.hunger = clamp(pet.hunger - 35)
        pet.happiness = clamp(pet.happiness + 5)
        if was_hungry:
            pet.health = clamp(pet.health + 3)
        if pet.hunger < 10:
            pet.chaos = clamp(pet.chaos + 8)
            pet.happiness = clamp(pet.happiness - 5)


class PlayAction(CareAction):
    name = "play"
    aliases = ("fun", "games", "toy")
    runs_while_asleep = False
    user_cooldown_minutes = 20
    per_hour_limit = 15

    def effect(self, pet):
        pet.happiness = clamp(pet.happiness + 12)
        pet.social = clamp(pet.social + 10)
        pet.energy = clamp(pet.energy - 15)
        pet.chaos = clamp(pet.chaos + 5)


class PetAction(CareAction):
    name = "pet"
    aliases = ("pat", "pats", "cuddle", "scritch", "scratch", "boop")
    user_cooldown_minutes = 10
    per_hour_limit = 30

    def effect(self, pet):
        pet.trust = clamp(pet.trust + 6)
        pet.social = clamp(pet.social + 5)
        pet.happiness = clamp(pet.happiness + 6)
        pet.energy = clamp(pet.energy - 2)


class CleanAction(CareAction):
    name = "clean"
    aliases = ("bath", "wash", "scrub", "tidy")
    runs_while_asleep = False
    user_cooldown_minutes = 60
    per_hour_limit = 5

    def effect(self, pet):
        pet.cleanliness = clamp(pet.cleanliness + 40)
        pet.happiness = clamp(pet.happiness - 6)
        pet.chaos = clamp(pet.chaos + 3)


class SleepAction(CareAction):
    name = "sleep"
    aliases = ("nap", "bed", "rest")
    global_cooldown_minutes = 120

    def precheck(self, ctx):
        if ctx.pet.asleep:
            return Outcome(responses.already_asleep(ctx.pet), accepted=False, record=False)
        return None

    def effect(self, pet):
        pet.asleep = True
        pet.happiness = clamp(pet.happiness + 2)


class WakeAction(CareAction):
    name = "wake"
    aliases = ("wakeup", "awake", "rise")
    global_cooldown_minutes = 60

    def precheck(self, ctx):
        if not ctx.pet.asleep:
            return Outcome(responses.already_awake(ctx.pet), accepted=False, record=False)
        return None

    def effect(self, pet):
        pet.asleep = False
        if pet.energy < 20:
            pet.happiness = clamp(pet.happiness - 3)
            pet.chaos = clamp(pet.chaos + 4)
