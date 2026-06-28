# Local testing

Prami runs entirely without Mastodon through the local CLI, which drives the **same** engine,
database, cooldowns, personality, and safety logic the live bot uses. Test everything here
before going online.

There are localized walkthroughs too: [local-testing.en.md](local-testing.en.md) (English) and
[local-testing.pt-br.md](local-testing.pt-br.md) (Português). This file is the full English
command reference.

## Database

The CLI uses `DATABASE_URL`. SQLite is perfect locally:

```bash
export DATABASE_URL="sqlite:///prami.db"     # PowerShell: $env:DATABASE_URL="sqlite:///prami.db"
```

In Docker, prefix any command with `docker compose run --rm prami`.

## Core commands

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

When an action is favourite- or boost-worthy, or it triggers a milestone, the CLI prints a
note under the reply so you can see the social logic firing.

## Time, state, and reset

```bash
python -m prami.cli tick --hours 4        # simulate decay
python -m prami.cli debug-state           # raw numbers (dev only)
python -m prami.cli reset --yes           # fresh slate (clears users, events, memories...)
```

## Relationships and nicknames

```bash
python -m prami.cli nickname Soup Wizard --user @alice@example.com
python -m prami.cli nickname clear --user @alice@example.com
python -m prami.cli relationship --user @alice@example.com   # counts, trust, bond level
```

## Teach / memory (moderated)

Set `ENABLE_TEACH_COMMAND=true` first.

```bash
python -m prami.cli teach '"Prami believes soup is a weather condition."' --user @alice@example.com
python -m prami.cli admin memories                 # list pending
python -m prami.cli admin approve-memory 1
python -m prami.cli admin reject-memory 2 "off-topic"
```

Nothing taught goes live until an admin approves it. The CLI grants you local admin.

## Community events

Set `ENABLE_EVENTS=true` (auto-start is random; force one for testing):

```bash
python -m prami.cli event-start snack_vote     # dev: force-start a specific event
python -m prami.cli event --user @alice@example.com
python -m prami.cli vote soup --user @alice@example.com
python -m prami.cli vote crunch --user @bob@example.com
python -m prami.cli event-complete             # dev: tally + apply the outcome
```

## Admin controls

```bash
python -m prami.cli admin status
python -m prami.cli admin pause
python -m prami.cli admin resume
python -m prami.cli admin set-favourites on
python -m prami.cli admin block @troll@bad.social
python -m prami.cli stats          # local operational metrics
```

## Interactive shell

```bash
python -m prami.cli shell
```

```
@alice feed
@bob play
@alice call me Soup Wizard
whois @alice
tick 2h
debug
exit
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```
