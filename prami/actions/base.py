from dataclasses import dataclass


@dataclass
class ActionContext:
    session: object
    pet: object
    user: object
    arg: str
    config: object
    settings: object
    now: object
    status_id: object = None


@dataclass
class Outcome:
    text: str
    accepted: bool = True
    record: bool = True
    address: bool = True
    favourite: bool = False
    boost: bool = False
    was_critical: bool = False
    visibility: str = None


class Action:
    name = ""
    aliases = ()
    phrase_aliases = ()
    admin_only = False
    runs_while_asleep = True
    user_cooldown_minutes = 0
    global_cooldown_minutes = 0
    per_hour_limit = None

    def enabled(self, config):
        return True

    def on_disabled(self, ctx):
        return Outcome(f"{ctx.pet.name} can't do that right now — it's turned off.", accepted=False, record=False)

    def precheck(self, ctx):
        return None

    def run(self, ctx):
        raise NotImplementedError
