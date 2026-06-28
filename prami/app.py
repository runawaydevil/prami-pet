import logging
import time

from . import engine
from . import repository as repo
from . import safety
from .config import config
from .db import create_all, init_engine, session_scope, wait_for_db
from .mastodon_client import PramiClient
from .parser import parse

log = logging.getLogger("prami.app")


def bootstrap():
    init_engine(config.database_url)
    wait_for_db()
    create_all()

    with session_scope() as session:
        pet = repo.get_or_create_pet(session, config)
        for acct in config.blocked_users:
            repo.block_user(session, acct)
        repo.log_event(session, pet.id, "startup", "prami started")
        log.info("Pet ready: %s the %s (day %s, mood %s)", pet.name, pet.species, pet.age_days, pet.mood)

    return PramiClient(config)


class Poller:
    def __init__(self, client):
        self.client = client
        self.last_id = None
        self.bot_acct = (config.bot_acct or client.me.acct).lstrip("@")
        self.bot_id = client.me.id

    def poll_once(self):
        mentions = self.client.fetch_mentions(since_id=self.last_id)
        for notif in reversed(mentions):
            if self.last_id is None or notif.id > self.last_id:
                self.last_id = notif.id
            self._handle(notif)

    def _handle(self, notif):
        status = getattr(notif, "status", None)
        if status is None:
            return

        account = notif.account
        if account.id == self.bot_id or account.acct.lstrip("@") == self.bot_acct:
            return

        sid = str(status.id)
        with session_scope() as session:
            if repo.is_status_processed(session, sid):
                return
            repo.mark_status_processed(session, sid)

            user = repo.get_or_create_user(
                session,
                acct=account.acct,
                mastodon_id=str(account.id),
                display_name=account.display_name or "",
            )
            pet = repo.get_pet(session)
            parsed = parse(status.content)
            command = parsed.name
            result = engine.handle(
                session, pet, user, command, config, status_id=sid, arg=parsed.arg
            )

        if result is None:
            return

        try:
            self.client.reply(status, f"@{account.acct} {result.text}", result.visibility)
            log.info("Replied to @%s (%s, accepted=%s)", account.acct, command, result.accepted)
        except Exception:
            log.exception("Failed to reply to @%s", account.acct)

        if result.boost:
            self._react(status, account, "boost")
        elif result.favourite:
            self._react(status, account, "favourite")

        if result.milestones:
            self._announce_milestones(result.milestones, status, account)

    def _announce_milestones(self, achieved, status, account):
        for milestone in achieved:
            if config.enable_milestone_posts:
                try:
                    self.client.post(milestone["text"], config.milestone_post_visibility)
                except Exception:
                    log.exception("Failed to post milestone %s", milestone["key"])
            if milestone.get("boost"):
                self._react(status, account, "boost")
            elif milestone.get("favourite"):
                self._react(status, account, "favourite")

    def _react(self, status, account, action):
        sid = str(status.id)
        visibility = getattr(status, "visibility", "public")
        with session_scope() as session:
            settings = repo.get_settings(session, config)
            user = repo.get_user(session, account.acct)
            check = safety.may_boost if action == "boost" else safety.may_favourite
            allowed, reason = check(session, settings, config, user, visibility, sid)
        if not allowed:
            log.info("Skipped %s of %s: %s", action, sid, reason)
            return

        try:
            (self.client.boost if action == "boost" else self.client.favourite)(status)
        except Exception:
            log.exception("Failed to %s %s", action, sid)
            return

        with session_scope() as session:
            if not repo.has_social_action(session, sid, action):
                pet = repo.get_pet(session)
                user = repo.get_user(session, account.acct)
                uid = user.id if user else None
                repo.record_social_action(session, pet.id, uid, sid, action, "worthy interaction")
                repo.log_event(session, pet.id, action, f"{action} of {sid} by @{account.acct}")
        log.info("%s %s by @%s", action.capitalize(), sid, account.acct)

    def run(self):
        log.info("Listening for mentions every %ss", config.poll_interval)
        while True:
            try:
                self.poll_once()
            except Exception:
                log.exception("Polling cycle failed")
            time.sleep(config.poll_interval)
