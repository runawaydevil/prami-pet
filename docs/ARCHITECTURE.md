# Architecture

Prami's behaviour is built as a set of small, self-contained **actions** wired together by an
**ActionRegistry** and run through a single command **pipeline**. There is no giant if/else
command handler, and parsing is kept separate from execution.

## Actions

Every command is an `Action` (in `prami/actions/`). An action declares its own metadata and
owns its own logic, so adding or changing a command is a local edit:

| Aspect | Where |
|---|---|
| command name + aliases | `name`, `aliases`, `phrase_aliases` |
| requires admin | `admin_only` |
| enabled by config | `enabled(config)` |
| per-user / global cooldown | `user_cooldown_minutes`, `global_cooldown_minutes` |
| hourly limit | `per_hour_limit` |
| runs while asleep | `runs_while_asleep` |
| early rejections (e.g. already asleep) | `precheck(ctx)` |
| input validation + state changes + response | `run(ctx)` |
| disabled message | `on_disabled(ctx)` |

`run(ctx)` returns an `Outcome` describing what happened:

```
Outcome(text, accepted, record, address, favourite, boost, was_critical, visibility)
```

`favourite`/`boost` are the action's side-effect eligibility; `was_critical` feeds milestone
and relationship logic; `record=False` marks informational actions (event/help/admin) that
shouldn't count as interactions; `visibility` lets an action override (admin replies direct).

Actions live one concept per file: `status.py`, `help.py`, `unknown.py`, `nickname.py`,
`teach.py`, `events.py` (event/help-event/vote), `admin.py`, and `care.py` (the six care
commands share a small `CareAction` base, since they only differ by their `effect(pet)`).

## ActionRegistry

`prami/actions/registry.py` builds the single registry (`REGISTRY`) at import time. It:

- registers every action,
- resolves a canonical command name to its action (`resolve`), falling back to the unknown
  action,
- resolves aliases and multi-word phrases to canonical names (`canonical`, `alias_map`,
  `phrase_map`),
- reports whether an action is enabled for a given config (`is_enabled`).

The parser reads its command vocabulary **from the registry** (`alias_map` / `phrase_map`), so
parsing and execution can never drift out of sync — aliases are defined once, on the action.

## The command pipeline

`engine.handle(...)` is the one pipeline both the CLI and the Mastodon poller call:

1. **Receive input** — actor, status id, arg, config.
2. **Normalize** — load runtime `settings`, build an `ActionContext`.
3. **Parse** — done upstream by `parser.parse` (mentions stripped, command + arg extracted).
4. **Resolve** — `REGISTRY.resolve(command)` returns the action (or the unknown action).
5. **Safety / moderation** — admin actions bypass; otherwise blocked users and paused state
   stop here.
6. **Cooldowns and rate limits** — global and per-user hourly caps, then the action's own
   cooldowns.
7. **Execute transactionally** — `action.precheck` then `action.run` mutate state inside the
   caller's DB session.
8. **Generate response** — the action returns the text in its `Outcome`.
9. **Apply side effects** — on an accepted, recorded outcome the pipeline records the
   interaction, updates the relationship, and checks milestones; favourite/boost eligibility
   ride back on the `Result`.
10. **Store processed status id** — handled by the Mastodon poller before dispatch, so the
    same status is never processed twice.

The pipeline returns a `Result(text, visibility, accepted, favourite, boost, milestones)`.

## One core path for CLI and Mastodon

Both entry points are thin and converge on `engine.handle`:

- **CLI** — `prami/cli.py` parses arguments, then calls `engine.handle` for every command,
  including admin (the CLI just grants the local operator admin first).
- **Mastodon** — `prami/app.py`'s poller normalizes the notification, calls `parser.parse`,
  then `engine.handle`, and finally executes the returned favourite/boost/milestone side
  effects through the Mastodon client.

No command logic is duplicated between them. Tests in `tests/test_actions.py` prove alias
resolution, disabled-command handling, admin-only gating, and that both the CLI and a
Mastodon-style parse run through the same registry and pipeline to the same result.

## Adding a command later

1. Write an `Action` subclass in `prami/actions/` with its metadata and `run`.
2. Register it in `build_registry()`.
3. That's it — the parser picks up its aliases, and the pipeline runs it. Add a focused test
   for the action's `run` and its eligibility.
