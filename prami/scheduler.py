import logging
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from . import autopost, decay, events, milestones, safety
from . import repository as repo
from .config import config
from .db import session_scope
from .models import utcnow

log = logging.getLogger("prami.scheduler")


def run_decay():
    with session_scope() as session:
        pet = repo.get_pet(session)
        if pet is None:
            return
        decay.tick(pet)
        log.info("Decay — mood=%s hunger=%s energy=%s clean=%s", pet.mood, pet.hunger, pet.energy, pet.cleanliness)


def run_autopost(client):
    posts = []
    with session_scope() as session:
        settings = repo.get_settings(session, config)
        pet = repo.get_pet(session)
        if pet is None or not safety.may_autopost(settings):
            return
        visibility = settings.autopost_visibility

        if config.enable_events:
            for outcome in events.expire_due(session, pet, utcnow()):
                milestones.award_event_completed(session, pet)
                posts.append(outcome)
            started = events.maybe_start(session, pet, config, utcnow())
            if started:
                posts.append(
                    f"{started.title} {started.description} "
                    f"Vote with '@{pet.name} vote <option>' — {events.options_text(started)}."
                )

        message = autopost.compose(session, pet, config)
        repo.log_event(session, pet.id, "autopost", message)
        posts.append(message)

    for text in posts:
        try:
            client.post(text, visibility)
        except Exception:
            log.exception("Failed to autopost")
    log.info("Autoposted %s message(s) (%s)", len(posts), visibility)


def run_maintenance():
    cutoff = utcnow() - timedelta(days=config.processed_retention_days)
    with session_scope() as session:
        removed = repo.prune_processed_statuses(session, cutoff)
    if removed:
        log.info("Pruned %s processed-status rows older than %s days", removed, config.processed_retention_days)


def build_scheduler(client):
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        run_decay, "interval", minutes=config.decay_interval, id="decay", max_instances=1, coalesce=True
    )
    if config.autopost_enabled:
        scheduler.add_job(
            run_autopost,
            "interval",
            minutes=config.autopost_interval,
            args=[client],
            id="autopost",
            max_instances=1,
            coalesce=True,
        )
    scheduler.add_job(
        run_maintenance, "interval", hours=24, id="maintenance", max_instances=1, coalesce=True
    )
    return scheduler
