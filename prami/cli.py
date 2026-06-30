import argparse
import sys

from . import decay
from . import engine
from . import repository as repo
from . import stats
from .config import config
from .db import create_all, init_engine, session_scope, wait_for_db
from .models import utcnow
from .parser import parse

DEFAULT_USER = "local@cli"
ACTION_COMMANDS = ["status", "feed", "play", "pet", "clean", "sleep", "wake", "help"]


def _open():
    init_engine(config.database_url)
    wait_for_db()
    create_all()
    with session_scope() as session:
        repo.get_or_create_pet(session, config)


def run_command(command, user_acct, arg=""):
    user_acct = (user_acct or DEFAULT_USER).lstrip("@")
    with session_scope() as session:
        pet = repo.get_pet(session)
        user = repo.get_or_create_user(session, user_acct)
        result = engine.handle(session, pet, user, command, config, arg=arg)
    if result is None:
        return {"text": f"({user_acct} is blocked or Prami is paused — nothing happens.)"}
    return {
        "text": result.text,
        "favourite": result.favourite,
        "boost": result.boost,
        "milestones": [m["text"] for m in result.milestones],
    }


def _format_result(result):
    line = result["text"]
    notes = []
    if result.get("boost"):
        notes.append("boost-worthy")
    elif result.get("favourite"):
        notes.append("favourite-worthy")
    if notes:
        line += f"\n  · ({', '.join(notes)})"
    for text in result.get("milestones", []):
        line += f"\n  * milestone: {text}"
    return line


def render_relationship(user):
    if user is None:
        return "No relationship on record for that user yet."
    rows = [
        ("acct", user.acct),
        ("nickname", user.nickname or "—"),
        ("bond_level", user.bond_level),
        ("trust_score", user.trust_score),
        ("total_interactions", user.total_interactions),
        ("feed/play/pet", f"{user.feed_count}/{user.play_count}/{user.pet_count}"),
        ("clean/sleep/wake", f"{user.clean_count}/{user.sleep_count}/{user.wake_count}"),
        ("first_seen", f"{user.first_seen:%Y-%m-%d %H:%M} UTC"),
        ("last_seen", f"{user.last_seen:%Y-%m-%d %H:%M} UTC"),
    ]
    width = max(len(label) for label, _ in rows)
    return "\n".join(f"{label.ljust(width)} : {value}" for label, value in rows)


def simulate_ticks(minutes):
    ticks = 1 if minutes <= 0 else max(1, minutes // config.decay_interval)
    with session_scope() as session:
        pet = repo.get_pet(session)
        for _ in range(ticks):
            decay.tick(pet)
        mood = pet.mood
    return ticks, mood


def render_debug(pet):
    if pet is None:
        return "No pet found."
    rows = [
        ("name", pet.name),
        ("hunger", pet.hunger),
        ("happiness", pet.happiness),
        ("energy", pet.energy),
        ("health", pet.health),
        ("cleanliness", pet.cleanliness),
        ("social", pet.social),
        ("trust", pet.trust),
        ("chaos", pet.chaos),
        ("asleep", pet.asleep),
        ("mood", pet.mood),
        ("age_days", pet.age_days),
        ("updated_at", f"{pet.updated_at:%Y-%m-%d %H:%M:%S} UTC"),
    ]
    width = max(len(label) for label, _ in rows)
    return "\n".join(f"{label.ljust(width)} : {value}" for label, value in rows)


def cmd_action(args):
    print(_format_result(run_command(args.command, args.user)))


def cmd_nickname(args):
    print(run_command("nickname", args.user, " ".join(args.name))["text"])


def cmd_relationship(args):
    acct = (args.user or DEFAULT_USER).lstrip("@")
    with session_scope() as session:
        print(render_relationship(repo.get_user(session, acct)))


def cmd_teach(args):
    print(run_command("teach", args.user, " ".join(args.content))["text"])


def cmd_event(args):
    print(run_command("event", args.user)["text"])


def cmd_vote(args):
    print(_format_result(run_command("vote", args.user, args.option)))


def cmd_event_start(args):
    from . import events

    with session_scope() as session:
        pet = repo.get_pet(session)
        template = next((t for t in events.TEMPLATES if t["key"] == args.key), None) if args.key else None
        event = events.start(session, pet, config, template=template)
        print(f"Started event: {event.title} ({events.options_text(event)})")


def cmd_event_complete(args):
    from . import events, milestones

    with session_scope() as session:
        pet = repo.get_pet(session)
        event = events.active(session)
        if event is None:
            print("No active event.")
            return
        outcome = events.complete(session, event, pet)
        milestones.award_event_completed(session, pet)
        print(f"Outcome: {outcome}")


def cmd_admin(args):
    acct = (args.user or DEFAULT_USER).lstrip("@")
    if acct.lower() not in [a.lower() for a in config.admin_accounts]:
        config.admin_accounts.append(acct)
    print(run_command("admin", acct, " ".join(args.args))["text"])


def cmd_debug(args):
    with session_scope() as session:
        print(render_debug(repo.get_pet(session)))


def cmd_stats(args):
    with session_scope() as session:
        settings = repo.get_settings(session, config)
        print(stats.text_report(session, config, settings, utcnow()))


def cmd_tick(args):
    minutes = args.hours * 60 + args.minutes
    ticks, mood = simulate_ticks(minutes)
    print(f"Simulated {ticks} decay tick(s). Prami is now {mood}.")


def cmd_reset(args):
    if not args.yes:
        answer = input("Reset local pet state to defaults? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Cancelled.")
            return
    with session_scope() as session:
        repo.reset_world(session, config)
    print("Prami has been reset to a fresh, slightly confused default state.")


def cmd_shell(args):
    print("Prami local shell — try '@alice feed', 'status', 'tick 2h', 'debug', or 'exit'.")
    while True:
        try:
            line = input("prami> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue

        low = line.lower()
        if low in ("exit", "quit"):
            break
        if low == "debug":
            with session_scope() as session:
                print(render_debug(repo.get_pet(session)))
            continue
        if low == "tick" or low.startswith("tick "):
            ticks, mood = simulate_ticks(_shell_minutes(line))
            print(f"(simulated {ticks} tick(s); mood: {mood})")
            continue
        if low.startswith("whois"):
            parts = line.split(None, 1)
            acct = (parts[1].lstrip("@") if len(parts) > 1 else DEFAULT_USER)
            with session_scope() as session:
                print(render_relationship(repo.get_user(session, acct)))
            continue

        if line.startswith("@"):
            head, _, rest = line.partition(" ")
            user_acct = head[1:]
            parsed = parse(rest)
        else:
            user_acct = DEFAULT_USER
            parsed = parse(line)

        print(f"Prami → {_format_result(run_command(parsed.name, user_acct, parsed.arg))}")


def _shell_minutes(line):
    parts = line.split()
    if len(parts) < 2:
        return 0
    token = parts[1].lower()
    try:
        if token.endswith("h"):
            return int(token[:-1]) * 60
        if token.endswith("m"):
            return int(token[:-1])
        return int(token)
    except ValueError:
        return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="prami.cli", description="Local testing CLI for Prami")
    sub = parser.add_subparsers(dest="cmd", required=True)

    for name in ACTION_COMMANDS:
        action = sub.add_parser(name, help=f"Run the '{name}' command as a user")
        action.add_argument("--user", default=None, help="Acting user, e.g. @alice@example.com")
        action.set_defaults(func=cmd_action, command=name)

    nickname = sub.add_parser("nickname", help="Set or clear your nickname (use 'clear' to remove)")
    nickname.add_argument("name", nargs="*", help="Nickname text, or 'clear'")
    nickname.add_argument("--user", default=None, help="Acting user, e.g. @alice@example.com")
    nickname.set_defaults(func=cmd_nickname)

    relationship = sub.add_parser("relationship", help="Inspect a user's relationship data (dev only)")
    relationship.add_argument("--user", default=None, help="User to inspect")
    relationship.set_defaults(func=cmd_relationship)

    teach = sub.add_parser("teach", help="Suggest a memory (needs ENABLE_TEACH_COMMAND=true)")
    teach.add_argument("content", nargs="*", help="The lore/fact/preference to suggest")
    teach.add_argument("--user", default=None, help="Acting user")
    teach.set_defaults(func=cmd_teach)

    admin_cmd = sub.add_parser("admin", help="Run an admin command (CLI grants local admin)")
    admin_cmd.add_argument("args", nargs="*", help="e.g. status / pause / memories / approve-memory 1")
    admin_cmd.add_argument("--user", default=None, help="Acting user")
    admin_cmd.set_defaults(func=cmd_admin)

    event = sub.add_parser("event", help="Show the active community event")
    event.add_argument("--user", default=None)
    event.set_defaults(func=cmd_event)

    vote = sub.add_parser("vote", help="Vote on the active event")
    vote.add_argument("option", help="The option key, e.g. soup")
    vote.add_argument("--user", default=None)
    vote.set_defaults(func=cmd_vote)

    event_start = sub.add_parser("event-start", help="Force-start an event (dev only)")
    event_start.add_argument("key", nargs="?", default=None, help="Optional template key")
    event_start.set_defaults(func=cmd_event_start)

    sub.add_parser("event-complete", help="Force-complete the active event (dev only)").set_defaults(
        func=cmd_event_complete
    )

    sub.add_parser("shell", help="Interactive local shell").set_defaults(func=cmd_shell)
    sub.add_parser("debug-state", help="Print raw internal state (dev only)").set_defaults(func=cmd_debug)
    sub.add_parser("stats", help="Show local operational metrics (admin/dev only)").set_defaults(func=cmd_stats)

    tick = sub.add_parser("tick", help="Simulate time passing (state decay)")
    tick.add_argument("--hours", type=int, default=0)
    tick.add_argument("--minutes", type=int, default=0)
    tick.set_defaults(func=cmd_tick)

    reset = sub.add_parser("reset", help="Reset local pet state to defaults")
    reset.add_argument("--yes", action="store_true", help="Skip the confirmation prompt")
    reset.set_defaults(func=cmd_reset)

    return parser


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    args = build_parser().parse_args(argv)
    _open()
    args.func(args)


if __name__ == "__main__":
    main()
