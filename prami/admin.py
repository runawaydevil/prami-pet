from . import memory
from . import repository as repo
from . import stats
from .actions.base import Outcome

VISIBILITIES = ("public", "unlisted", "private", "direct")
ADMIN_VISIBILITY = "direct"


def run(ctx):
    config, user = ctx.config, ctx.user
    if not config.is_admin(user.acct):
        if config.admin_refuse_nonadmin:
            return Outcome(
                "That's an admin-only command.",
                accepted=False, record=False, address=False, visibility=ADMIN_VISIBILITY,
            )
        return None

    parts = ctx.arg.split()
    sub = parts[0].lower() if parts else "help"
    rest = " ".join(parts[1:]).strip()

    if sub == "stats":
        text = stats.text_report(ctx.session, ctx.config, ctx.settings, ctx.now)
    else:
        text = _dispatch(ctx.session, ctx.pet, ctx.settings, sub, rest)
    repo.log_event(ctx.session, ctx.pet.id, "admin", f"{user.acct}: {ctx.arg}".strip())
    return Outcome(text, record=False, address=False, visibility=ADMIN_VISIBILITY)


def _dispatch(session, pet, settings, sub, rest):
    if sub == "status":
        return _status(session, settings)
    if sub == "pause":
        settings.paused = True
        return "Prami is paused — it will stop reacting until you resume it."
    if sub == "resume":
        settings.paused = False
        return "Prami is back. It missed you, probably."
    if sub == "set-visibility":
        if rest in VISIBILITIES:
            settings.default_visibility = rest
            return f"Default reply visibility set to {rest}."
        return f"Visibility must be one of: {', '.join(VISIBILITIES)}."
    if sub == "set-autopost":
        settings.autopost_enabled = _on(rest)
        return f"Autoposts {_state(settings.autopost_enabled)}."
    if sub == "set-favourites":
        settings.favourites_enabled = _on(rest)
        return f"Favourites {_state(settings.favourites_enabled)}."
    if sub == "set-boosts":
        settings.boosts_enabled = _on(rest)
        return f"Boosts {_state(settings.boosts_enabled)}."
    if sub == "blocked-users":
        return _blocked(session)
    if sub == "block" and rest:
        repo.block_user(session, rest)
        return f"Blocked {rest.lstrip('@')}."
    if sub == "unblock" and rest:
        target = repo.get_user(session, rest)
        if target:
            target.blocked = False
        return f"Unblocked {rest.lstrip('@')}."
    if sub == "memories" or (sub == "memory-list" and rest in ("", "pending")):
        return _memory_list(session, "pending")
    if sub == "memory-list":
        return _memory_list(session, rest)
    if sub == "approve-memory" and rest:
        return _review(session, rest, approve=True)
    if sub == "reject-memory" and rest:
        return _review(session, rest, approve=False)
    return _help()


def _on(value):
    return value.strip().lower() in ("on", "true", "yes", "1", "enable", "enabled")


def _state(enabled):
    return "enabled" if enabled else "disabled"


def _status(session, settings):
    pending = len(memory.by_status(session, "pending"))
    approved = len(memory.by_status(session, "approved"))
    return (
        f"paused={settings.paused} · autopost={_state(settings.autopost_enabled)} · "
        f"favourites={_state(settings.favourites_enabled)} · boosts={_state(settings.boosts_enabled)} · "
        f"visibility={settings.default_visibility} · memories: {pending} pending, {approved} approved"
    )


def _blocked(session):
    from .models import User
    from sqlalchemy import select

    blocked = list(session.scalars(select(User).where(User.blocked.is_(True))))
    if not blocked:
        return "No blocked users."
    return "Blocked: " + ", ".join(u.acct for u in blocked)


def _memory_list(session, status):
    status = status if status in ("pending", "approved", "rejected") else "pending"
    items = memory.by_status(session, status)
    if not items:
        return f"No {status} memories."
    lines = [f"#{m.id} [{m.category}] {m.content}" for m in items[:10]]
    return f"{status.capitalize()} memories:\n" + "\n".join(lines)


def _review(session, rest, approve):
    parts = rest.split(None, 1)
    try:
        suggestion_id = int(parts[0])
    except ValueError:
        return "Usage: approve-memory <id> | reject-memory <id> [reason]"

    if approve:
        result = memory.approve(session, suggestion_id, "admin")
        return f"Approved memory #{suggestion_id}." if result else f"No pending memory #{suggestion_id}."

    reason = parts[1] if len(parts) > 1 else ""
    result = memory.reject(session, suggestion_id, "admin", reason)
    return f"Rejected memory #{suggestion_id}." if result else f"No pending memory #{suggestion_id}."


def _help():
    return (
        "Admin commands: status · stats · pause · resume · set-visibility <v> · "
        "set-autopost on|off · set-favourites on|off · set-boosts on|off · "
        "blocked-users · block <user> · unblock <user> · memories · "
        "memory-list pending|approved · approve-memory <id> · reject-memory <id> [reason]"
    )
