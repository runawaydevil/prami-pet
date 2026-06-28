from sqlalchemy import select

from . import repository as repo
from .models import Milestone
from .relationships import CARE_COMMANDS


def _already(session, pet_id, user_id, key):
    stmt = select(Milestone).where(Milestone.pet_id == pet_id, Milestone.key == key)
    stmt = stmt.where(Milestone.user_id.is_(None) if user_id is None else Milestone.user_id == user_id)
    return session.scalars(stmt).first() is not None


def check(session, pet, user, command, was_critical):
    found = []

    def award(key, scope, user_id, text, favourite=False, boost=False):
        if _already(session, pet.id, user_id, key):
            return
        session.add(Milestone(pet_id=pet.id, user_id=user_id, key=key, scope=scope))
        session.flush()
        found.append({"key": key, "scope": scope, "text": text, "favourite": favourite, "boost": boost})

    name = pet.name

    if user.total_interactions == 1:
        award("first_interaction", "user", user.id, f"A new face met {name} today. Welcome, @{user.acct}.")
    if user.total_interactions == 10:
        award("user_10", "user", user.id, f"@{user.acct} has looked after {name} ten times now. {name} noticed.")
    if user.total_interactions == 25:
        award("user_25", "user", user.id, f"@{user.acct} hit 25 interactions with {name}. That's basically family.")
    if was_critical and command in CARE_COMMANDS:
        award("first_critical_save", "user", user.id,
              f"@{user.acct} helped {name} in a rough moment. {name} will remember this.", favourite=True)
    if user.bond_level == "trusted":
        award("reached_trusted", "user", user.id, f"@{user.acct} and {name} reached 'trusted'. Hard-won and real.")
    if user.bond_level == "friend":
        award("reached_friend", "user", user.id, f"@{user.acct} is officially {name}'s friend now. Big deal, quietly.")

    if command == "feed" and repo.count_interactions_total(session, "feed") == 1:
        award("first_feeding", "community", None, f"{name} was fed for the very first time. A historic snack.", favourite=True)
    if command == "clean" and repo.count_interactions_total(session, "clean") == 1:
        award("first_bath_survived", "community", None, f"{name} survived its first bath. Furious, clean, alive.")
    if repo.count_interactions_total(session) >= 100:
        award("100_interactions", "community", None, f"The community has cared for {name} 100 times. Thank you, all of you.", favourite=True, boost=True)
    if pet.age_days >= 7:
        award("7_days_alive", "community", None, f"{name} has been alive for a week. Seven whole days of tiny chaos.")
    if was_critical and command == "feed":
        award("saved_from_critical_hunger", "community", None, f"{name} was saved from going truly hungry. Good work, everyone.", favourite=True)
    if pet.chaos >= 100:
        award("chaos_100", "community", None, f"{name}'s chaos hit maximum and nobody was harmed. Mostly.")

    return found


def award_event_completed(session, pet):
    if _already(session, pet.id, None, "first_event_completed"):
        return None
    session.add(Milestone(pet_id=pet.id, user_id=None, key="first_event_completed", scope="community"))
    session.flush()
    return {"key": "first_event_completed", "scope": "community",
            "text": f"{pet.name} completed its first community event. Democracy survived.",
            "favourite": False, "boost": False}
