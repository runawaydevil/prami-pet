from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    species: Mapped[str] = mapped_column(String(120))
    personality: Mapped[str] = mapped_column(String(255))

    hunger: Mapped[int] = mapped_column(default=40)
    happiness: Mapped[int] = mapped_column(default=60)
    energy: Mapped[int] = mapped_column(default=70)
    health: Mapped[int] = mapped_column(default=90)
    cleanliness: Mapped[int] = mapped_column(default=70)
    social: Mapped[int] = mapped_column(default=50)
    trust: Mapped[int] = mapped_column(default=30)
    chaos: Mapped[int] = mapped_column(default=20)

    asleep: Mapped[bool] = mapped_column(Boolean, default=False)
    mood: Mapped[str] = mapped_column(String(40), default="content")

    last_autopost_category: Mapped[str | None] = mapped_column(String(40), nullable=True)
    last_autopost_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_decay_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    born_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)

    @property
    def age_days(self):
        return max(0, (utcnow() - self.born_at).days)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    acct: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    mastodon_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    display_name: Mapped[str] = mapped_column(String(255), default="")
    nickname: Mapped[str | None] = mapped_column(String(32), nullable=True)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    total_interactions: Mapped[int] = mapped_column(default=0)
    feed_count: Mapped[int] = mapped_column(default=0)
    play_count: Mapped[int] = mapped_column(default=0)
    pet_count: Mapped[int] = mapped_column(default=0)
    clean_count: Mapped[int] = mapped_column(default=0)
    sleep_count: Mapped[int] = mapped_column(default=0)
    wake_count: Mapped[int] = mapped_column(default=0)

    trust_score: Mapped[int] = mapped_column(default=0)
    bond_level: Mapped[str] = mapped_column(String(20), default="stranger")
    last_milestone_seen: Mapped[str | None] = mapped_column(String(60), nullable=True)

    first_seen: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    command: Mapped[str] = mapped_column(String(40), index=True)
    status_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    accepted: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)

    user: Mapped[User] = relationship()


class Cooldown(Base):
    __tablename__ = "cooldowns"
    __table_args__ = (UniqueConstraint("pet_id", "user_id", "command", name="uq_cooldown_scope"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    command: Mapped[str] = mapped_column(String(40))
    last_used_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class ProcessedStatus(Base):
    __tablename__ = "processed_statuses"

    status_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int | None] = mapped_column(ForeignKey("pets.id"), nullable=True)
    kind: Mapped[str] = mapped_column(String(60), index=True)
    detail: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    paused: Mapped[bool] = mapped_column(Boolean, default=False)
    autopost_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    favourites_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    boosts_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    default_visibility: Mapped[str] = mapped_column(String(20), default="unlisted")
    autopost_visibility: Mapped[str] = mapped_column(String(20), default="unlisted")


class SocialAction(Base):
    __tablename__ = "social_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    status_id: Mapped[str] = mapped_column(String(64), index=True)
    action: Mapped[str] = mapped_column(String(20), index=True)
    reason: Mapped[str] = mapped_column(String(120), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)


class MemorySuggestion(Base):
    __tablename__ = "memory_suggestions"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), index=True)
    submitted_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(20), default="lore")
    status: Mapped[str] = mapped_column(String(12), default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(String(180), nullable=True)


class CommunityEvent(Base):
    __tablename__ = "community_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), index=True)
    key: Mapped[str] = mapped_column(String(60))
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(255))
    options: Mapped[str] = mapped_column(Text, default="{}")
    status: Mapped[str] = mapped_column(String(12), default="active", index=True)
    outcome: Mapped[str | None] = mapped_column(String(255), nullable=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    ends_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class EventVote(Base):
    __tablename__ = "event_votes"
    __table_args__ = (UniqueConstraint("event_id", "user_id", name="uq_event_vote"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("community_events.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    option: Mapped[str] = mapped_column(String(40))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Milestone(Base):
    __tablename__ = "milestones"
    __table_args__ = (UniqueConstraint("pet_id", "user_id", "key", name="uq_milestone"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    key: Mapped[str] = mapped_column(String(60))
    scope: Mapped[str] = mapped_column(String(12), default="community")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
