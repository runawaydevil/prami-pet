from datetime import timedelta

from . import milestones
from . import relationships
from . import repository as repo
from . import responses
from .actions.base import ActionContext
from .actions.registry import REGISTRY
from .models import utcnow
from .result import Result


def handle(session, pet, user, command, config, status_id=None, now=None, arg=""):
    now = now or utcnow()
    settings = repo.get_settings(session, config)
    action = REGISTRY.resolve(command or "unknown")
    ctx = ActionContext(session, pet, user, arg or "", config, settings, now, status_id)

    if action.admin_only:
        return _finalize(ctx, action, action.run(ctx))

    if user.blocked or settings.paused:
        return None

    if repo.count_global_interactions_last_hour(session, now) >= config.max_global_hour:
        repo.log_event(session, pet.id, "rate_block_global", f"{user.acct} hit the global cap")
        return None
    if repo.count_user_interactions_last_hour(session, user.id, now) >= config.max_per_user_hour:
        return Result(responses.too_much(pet), settings.default_visibility, False)

    if not action.enabled(config):
        return _finalize(ctx, action, action.on_disabled(ctx))

    if pet.asleep and not action.runs_while_asleep:
        return Result(responses.too_sleepy(action.name, pet), settings.default_visibility, False)

    early = action.precheck(ctx)
    if early is not None:
        return _finalize(ctx, action, early)

    reason = _cooldown_reason(session, pet, user, action, now)
    if reason:
        return Result(responses.cooldown(action.name, reason, pet), settings.default_visibility, False)

    return _finalize(ctx, action, action.run(ctx))


def _finalize(ctx, action, outcome):
    if outcome is None:
        return None

    session, pet, user = ctx.session, ctx.pet, ctx.user
    achieved = []

    if outcome.accepted:
        _touch_cooldowns(session, pet, user, action, ctx.now)
        if outcome.record:
            repo.record_interaction(session, pet.id, user.id, action.name, ctx.status_id, True)
            relationships.record(user, action.name, pet, outcome.was_critical)
            user.last_seen = utcnow()
            achieved = milestones.check(session, pet, user, action.name, outcome.was_critical)

    text = responses.maybe_address(outcome.text, user) if outcome.address else outcome.text
    visibility = outcome.visibility or ctx.settings.default_visibility
    return Result(text, visibility, outcome.accepted, outcome.favourite, outcome.boost, achieved)


def _cooldown_reason(session, pet, user, action, now):
    if action.global_cooldown_minutes:
        cd = repo.get_cooldown(session, pet.id, None, action.name)
        if cd and now - cd.last_used_at < timedelta(minutes=action.global_cooldown_minutes):
            return "global"

    if action.user_cooldown_minutes:
        cd = repo.get_cooldown(session, pet.id, user.id, action.name)
        if cd and now - cd.last_used_at < timedelta(minutes=action.user_cooldown_minutes):
            return "user"

    if action.per_hour_limit is not None:
        if repo.count_command_last_hour(session, action.name, now) >= action.per_hour_limit:
            return "busy"

    return None


def _touch_cooldowns(session, pet, user, action, now):
    if action.user_cooldown_minutes:
        repo.touch_cooldown(session, pet.id, user.id, action.name, now)
    if action.global_cooldown_minutes:
        repo.touch_cooldown(session, pet.id, None, action.name, now)
