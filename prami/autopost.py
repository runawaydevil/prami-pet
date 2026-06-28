import random

from . import events
from . import memory
from . import responses
from . import templates
from .models import utcnow

FLAVOR = ("weird_observation", "existential", "community_appreciation")


def choose_category(session, pet, config):
    options = [responses.autopost_group(pet), *FLAVOR]

    if config.enable_events and events.active(session) is not None:
        options += ["active_event_reminder", "active_event_reminder"]
    if memory.by_status(session, "approved"):
        options.append("approved_memory_callback")

    fresh = [c for c in options if c != pet.last_autopost_category]
    return random.choice(fresh or options)


def render(session, pet, category):
    if category == "active_event_reminder":
        event = events.active(session)
        if event is not None:
            return templates.AUTOPOST_EVENT_REMINDER.format(
                name=pet.name, title=event.title, options=events.options_text(event)
            )
    if category == "approved_memory_callback":
        suggestion = memory.random_approved(session)
        if suggestion is not None:
            return templates.AUTOPOST_MEMORY_CALLBACK.format(name=pet.name, memory=suggestion.content)

    pool = responses.AUTOPOST.get(category) or responses.AUTOPOST["weird_observation"]
    return responses._render(pool, pet)


def compose(session, pet, config):
    category = choose_category(session, pet, config)
    text = render(session, pet, category)
    pet.last_autopost_category = category
    pet.last_autopost_at = utcnow()
    return text
