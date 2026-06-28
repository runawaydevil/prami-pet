from datetime import timedelta

from sqlalchemy import delete, func, select

from .models import (
    Cooldown,
    CommunityEvent,
    Event,
    EventVote,
    Interaction,
    MemorySuggestion,
    Milestone,
    Pet,
    ProcessedStatus,
    Settings,
    SocialAction,
    User,
    utcnow,
)


def get_pet(session):
    return session.scalars(select(Pet).order_by(Pet.id)).first()


def get_or_create_pet(session, config):
    pet = get_pet(session)
    if pet is None:
        pet = Pet(
            name=config.pet_name,
            species=config.pet_species,
            personality=config.pet_personality,
        )
        session.add(pet)
        session.flush()
    return pet


def get_user(session, acct):
    return session.scalars(select(User).where(User.acct == acct.lstrip("@"))).first()


def get_or_create_user(session, acct, mastodon_id=None, display_name=""):
    acct = acct.lstrip("@")
    user = session.scalars(select(User).where(User.acct == acct)).first()
    if user is None:
        user = User(acct=acct, mastodon_id=mastodon_id, display_name=display_name)
        session.add(user)
        session.flush()
    else:
        user.last_seen = utcnow()
        if mastodon_id and not user.mastodon_id:
            user.mastodon_id = mastodon_id
        if display_name:
            user.display_name = display_name
    return user


def block_user(session, acct):
    user = get_or_create_user(session, acct)
    user.blocked = True
    return user


def is_status_processed(session, status_id):
    return session.get(ProcessedStatus, str(status_id)) is not None


def mark_status_processed(session, status_id):
    session.add(ProcessedStatus(status_id=str(status_id)))


def prune_processed_statuses(session, before):
    result = session.execute(delete(ProcessedStatus).where(ProcessedStatus.created_at < before))
    return result.rowcount or 0


def record_interaction(session, pet_id, user_id, command, status_id, accepted):
    session.add(
        Interaction(
            pet_id=pet_id,
            user_id=user_id,
            command=command,
            status_id=str(status_id) if status_id else None,
            accepted=accepted,
        )
    )


def _since(now):
    return (now or utcnow()) - timedelta(hours=1)


def count_user_interactions_last_hour(session, user_id, now=None):
    stmt = (
        select(func.count())
        .select_from(Interaction)
        .where(
            Interaction.user_id == user_id,
            Interaction.accepted.is_(True),
            Interaction.created_at >= _since(now),
        )
    )
    return session.scalar(stmt) or 0


def count_global_interactions_last_hour(session, now=None):
    stmt = (
        select(func.count())
        .select_from(Interaction)
        .where(
            Interaction.accepted.is_(True),
            Interaction.created_at >= _since(now),
        )
    )
    return session.scalar(stmt) or 0


def count_interactions_total(session, command=None):
    stmt = select(func.count()).select_from(Interaction).where(Interaction.accepted.is_(True))
    if command:
        stmt = stmt.where(Interaction.command == command)
    return session.scalar(stmt) or 0


def count_command_last_hour(session, command, now=None):
    stmt = (
        select(func.count())
        .select_from(Interaction)
        .where(
            Interaction.command == command,
            Interaction.accepted.is_(True),
            Interaction.created_at >= _since(now),
        )
    )
    return session.scalar(stmt) or 0


def get_cooldown(session, pet_id, user_id, command):
    stmt = select(Cooldown).where(
        Cooldown.pet_id == pet_id,
        Cooldown.command == command,
        Cooldown.user_id.is_(None) if user_id is None else Cooldown.user_id == user_id,
    )
    return session.scalars(stmt).first()


def touch_cooldown(session, pet_id, user_id, command, now=None):
    now = now or utcnow()
    cd = get_cooldown(session, pet_id, user_id, command)
    if cd is None:
        session.add(Cooldown(pet_id=pet_id, user_id=user_id, command=command, last_used_at=now))
    else:
        cd.last_used_at = now


def log_event(session, pet_id, kind, detail=""):
    session.add(Event(pet_id=pet_id, kind=kind, detail=detail))


def get_settings(session, config):
    settings = session.scalars(select(Settings).order_by(Settings.id)).first()
    if settings is None:
        settings = Settings(
            autopost_enabled=config.autopost_enabled,
            favourites_enabled=config.enable_favourites,
            boosts_enabled=config.enable_boosts,
            default_visibility=config.default_visibility,
            autopost_visibility=config.autopost_visibility,
        )
        session.add(settings)
        session.flush()
    return settings


def has_social_action(session, status_id, action):
    stmt = select(SocialAction).where(
        SocialAction.status_id == str(status_id), SocialAction.action == action
    )
    return session.scalars(stmt).first() is not None


def record_social_action(session, pet_id, user_id, status_id, action, reason=""):
    session.add(
        SocialAction(
            pet_id=pet_id,
            user_id=user_id,
            status_id=str(status_id),
            action=action,
            reason=reason,
        )
    )


def count_social_actions(session, action, since, user_id=None):
    stmt = select(func.count()).select_from(SocialAction).where(
        SocialAction.action == action, SocialAction.created_at >= since
    )
    if user_id is not None:
        stmt = stmt.where(SocialAction.user_id == user_id)
    return session.scalar(stmt) or 0


def last_social_action_at(session, action):
    stmt = select(func.max(SocialAction.created_at)).where(SocialAction.action == action)
    return session.scalar(stmt)


def reset_world(session, config):
    for model in (
        EventVote,
        CommunityEvent,
        Milestone,
        MemorySuggestion,
        SocialAction,
        Cooldown,
        Interaction,
        Event,
        ProcessedStatus,
        Settings,
        User,
    ):
        session.execute(delete(model))
    session.execute(delete(Pet))
    session.flush()
    get_settings(session, config)
    return get_or_create_pet(session, config)
