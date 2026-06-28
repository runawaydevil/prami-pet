# Admin commands

Admins steer Prami at runtime through mentions, and the same actions are available locally
through the CLI for testing.

## Configuring admins

List admin accounts in `.env`, comma-separated:

```
ADMIN_ACCOUNTS=admin@example.com,mod@example.org
```

Only these accounts can run admin commands. Non-admins who try are ignored silently by
default, or get a short refusal if `ADMIN_REFUSE_NONADMIN=true`. Every admin action is logged
to the events table, and admin replies are sent as direct messages.

## Commands (via Mastodon mention)

```
@prami admin status
@prami admin stats
@prami admin pause
@prami admin resume
@prami admin set-visibility public|unlisted|private|direct
@prami admin set-autopost on|off
@prami admin set-favourites on|off
@prami admin set-boosts on|off
@prami admin blocked-users
@prami admin block @user@example.com
@prami admin unblock @user@example.com
@prami admin memories
@prami admin memory-list pending|approved
@prami admin approve-memory <id>
@prami admin reject-memory <id> [reason]
```

- **status** — one-line summary: paused, autopost/favourites/boosts state, default
  visibility, and pending/approved memory counts.
- **stats** — a fuller local operational report (see below).
- **pause / resume** — stop or restart all of Prami's reactions instantly.
- **set-visibility / set-autopost / set-favourites / set-boosts** — toggle runtime behaviour
  without redeploying. These override the `.env` defaults until changed again.
- **block / unblock / blocked-users** — manage the block list at runtime.
- **memories / memory-list / approve-memory / reject-memory** — review the teach queue.

Runtime toggles are stored in the `settings` table, so they survive restarts.

## Local metrics (stats)

`@prami admin stats` (and `python -m prami.cli stats`) prints a local operational report. It
is **local-only and admin-only** — there is no external analytics, nothing is phoned home, and
no sensitive personal data is collected. It only counts game activity already in the database,
and admin replies go out direct, so it is never exposed publicly.

It reports:

- **uptime** — time since the bot process last started (`—` if started only via the CLI)
- **total interactions** and **interactions in the last 24h**
- **unique users in the last 24h**
- **current mood** and **current critical stats** (any survival stat in the danger zone)
- **autonomous posts**, **favourites**, and **boosts** in the last 24h
- the **active event**, if any
- **pending memory suggestions** and **blocked users** count
- the **most-used commands**
- **last decay run** and **last autonomous post**
- **database connection status**

Example:

```
Prami — local stats
uptime: 3d 6h 41m
mood: content · critical: none
stats: hunger=38 energy=64 health=92 clean=55 social=47
interactions: 1284 total · 73 in 24h · 21 unique users 24h
top commands: pet:511, feed:402, status:240, play:88, clean:31
autoposts 24h: 6 · favourites 24h: 4 · boosts 24h: 0
active event: Prami needs help choosing a snack.
pending memories: 2 · blocked users: 1
last decay: 2026-06-28 22:05 UTC
last autopost: 2026-06-28 20:11 UTC (lonely)
database: connected (postgresql)
```

## The same actions locally (CLI)

The local CLI grants admin to whoever runs it, so you can exercise the real admin handler
without configuring accounts:

```bash
python -m prami.cli admin status
python -m prami.cli admin pause
python -m prami.cli admin set-favourites on
python -m prami.cli admin memories
python -m prami.cli admin approve-memory 1
python -m prami.cli admin reject-memory 2 "off-topic"
python -m prami.cli admin block @troll@bad.social
python -m prami.cli stats
```

See [LOCAL_TESTING.md](LOCAL_TESTING.md) for the full local workflow.
