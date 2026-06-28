# Local testing (no Mastodon needed)

Prami ships with a local CLI so you can play with the pet as a game and personality
engine before ever connecting it to Mastodon. The CLI drives the **same** parser, game
engine, cooldowns, database and response generator the bot uses — it is not a separate
mock.

By default it uses whatever `DATABASE_URL` is set (SQLite is perfect locally):

```bash
export DATABASE_URL="sqlite:///prami.db"   # Windows PowerShell: $env:DATABASE_URL="sqlite:///prami.db"
```

## One-shot commands

```bash
python -m prami.cli status
python -m prami.cli feed  --user @alice@example.com
python -m prami.cli play  --user @bob@example.com
python -m prami.cli pet   --user @alice@example.com
python -m prami.cli clean --user @alice@example.com
python -m prami.cli sleep --user @alice@example.com
python -m prami.cli wake  --user @alice@example.com
python -m prami.cli help
```

`--user` is optional; without it a default local user is used. Each user has its own
cooldowns, just like real accounts.

## Nicknames and relationships

Prami remembers lightweight, game-only data about each user (interaction counts, a
per-user trust score, and a bond level: stranger → familiar → trusted → friend →
beloved menace). Kind, frequent users bond faster; helping during a critical state is
worth extra trust.

```bash
python -m prami.cli nickname Soup Wizard --user @alice@example.com   # set a nickname
python -m prami.cli nickname clear --user @alice@example.com         # remove it
python -m prami.cli relationship --user @alice@example.com           # inspect (dev only)
```

Nicknames are sanitized (max 32 chars, no URLs, mentions, HTML, or line breaks) and have a
short cooldown. Prami uses a set nickname occasionally in replies, a little more often for
high-bond users. Raw relationship numbers only show in `relationship`, never in normal
replies.

## Social features (teach, events, admin)

These need their flags on (`ENABLE_TEACH_COMMAND`, `ENABLE_EVENTS`). The CLI grants you local
admin. Full reference: [LOCAL_TESTING.md](LOCAL_TESTING.md).

```bash
python -m prami.cli teach '"Prami believes soup is weather."' --user @alice@example.com
python -m prami.cli admin memories
python -m prami.cli admin approve-memory 1
python -m prami.cli event-start snack_vote
python -m prami.cli vote soup --user @alice@example.com
python -m prami.cli event-complete
python -m prami.cli admin status
```

When an action is favourite/boost-worthy or hits a milestone, the CLI notes it under the reply.

## Interactive shell

```bash
python -m prami.cli shell
```

Then type interactions as if they were mentions:

```
@alice feed
@bob play
@alice status
@charlie pet
tick 2h
debug
exit
```

You can also set a nickname (`@alice call me Soup Wizard`) and inspect a user with
`whois @alice`.

Inside the shell: `tick`, `tick 30m`, `tick 3h` simulate time; `debug` prints raw state;
`exit` or `quit` leaves.

## Inspect raw state (dev only)

```bash
python -m prami.cli debug-state
```

Prints the raw numbers — hunger, happiness, energy, health, cleanliness, social, trust,
chaos, asleep, mood and the last updated timestamp. Normal users only ever see the
narrative `status`, never these numbers.

## Simulate time passing

```bash
python -m prami.cli tick                 # one decay step
python -m prami.cli tick --hours 3
python -m prami.cli tick --minutes 30
```

This applies the exact same decay logic the scheduler runs. One step equals
`STATE_DECAY_INTERVAL_MINUTES` of real time, so `--hours 3` applies as many steps as the
scheduler would over three hours.

## Reset

```bash
python -m prami.cli reset          # asks for confirmation
python -m prami.cli reset --yes    # no prompt
```

Resets the pet to defaults and clears interactions, cooldowns, events and processed
statuses. User records are kept.

## Inside Docker Compose

The same commands work in the container, against the Compose Postgres:

```bash
docker compose run --rm prami python -m prami.cli status
docker compose run --rm prami python -m prami.cli feed --user @alice@example.com
docker compose run --rm prami python -m prami.cli shell
docker compose run --rm prami python -m prami.cli tick --hours 4
docker compose run --rm prami python -m prami.cli debug-state
```
