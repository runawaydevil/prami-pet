# Moderation and safety

Prami is built to be quiet, hard to abuse, and easy to host responsibly. A single safety
module (`prami/safety.py`) is the gatekeeper for every outward action. Nothing the public
says becomes Prami's voice without a human approving it.

## What the safety module decides

Before Prami does any of the following, the safety layer must allow it:

| Action | Checks applied |
|---|---|
| **reply** | not paused, user not blocked, within per-user and global hourly limits |
| **favourite** | favourites enabled, not paused, user not blocked, status not private/direct (unless allowed), not already favourited, within hourly and per-user-daily caps |
| **boost** | boosts enabled, not paused, user not blocked, status public only, not already boosted, within daily cap, and at least N hours since the last boost |
| **store memory** | the teach command is enabled, content passes sanitation |
| **use a nickname** | nickname passes sanitation (length, no URLs/mentions/HTML) |
| **autonomous post** | autoposts enabled and not paused |

## Core protections

- **Blocked users** — accounts in `BLOCKED_USERS`, or blocked at runtime by an admin, are
  ignored silently. Prami never replies to, favourites, or boosts them.
- **Rate limits** — per-user and global hourly command caps, per-command cooldowns, plus
  separate caps for favourites and boosts.
- **Duplicate protection** — every processed status ID is recorded, so Prami never reacts to
  the same mention twice. Favourited and boosted status IDs are stored too, so it never
  favourites or boosts the same status twice.
- **No loops** — Prami never replies to its own posts or acts on its own account.
- **Pause switch** — an admin can pause Prami instantly; while paused it stops replying,
  reacting, and autoposting (admins can still run commands to resume it).
- **Unlisted by default** — replies, autonomous posts, and milestone posts default to
  unlisted so Prami never floods public or federated timelines.

## Favourites

Favourites are Prami's lightweight "I noticed that" signal, and the preferred reaction for
ordinary good moments — feeding a starving Prami, petting a lonely one, cleaning a filthy
one, hitting a milestone. They are **off unless `ENABLE_FAVOURITES=true`**, capped per hour
and per user per day, and never applied to private/direct statuses unless
`ALLOW_FAVOURITE_PRIVATE=true`.

## Boosts

Boosts are deliberately **rare and off by default** (`ENABLE_BOOSTS=false`). A boost amplifies
someone else's post to all of Prami's followers, so it is reserved for genuinely special
moments — saving Prami from a critical state, a major community milestone, or a completed
event. Even when enabled, boosts are bounded by `MAX_BOOSTS_PER_DAY`,
`MIN_HOURS_BETWEEN_BOOSTS`, and `BOOST_ONLY_PUBLIC_STATUSES=true`. Prami always prefers a
favourite over a boost for everyday positive interactions.

## Teach / memory approval

Users can *suggest* lore with the teach command, but **nothing they submit ever becomes
active automatically**. Every suggestion is stored as `pending` and only influences Prami
after an admin approves it. Content is sanitized (length-limited, no HTML, no mentions, and
no URLs unless `MEMORY_ALLOW_URLS=true`). Rejected suggestions are kept for the record but
are never publicly shamed. The whole feature is off unless `ENABLE_TEACH_COMMAND=true`.

This gating exists because letting the public write what Prami says is a moderation hazard —
it could otherwise become a vector for slurs, harassment, or spam in the pet's mouth.

## Content sanitation

`prami/sanitize.py` cleans user-provided text (nicknames and memory suggestions): it strips
HTML, collapses whitespace and line breaks, rejects mentions and (by default) URLs, and
enforces length limits. Sanitized values are the only user text Prami will ever repeat.
