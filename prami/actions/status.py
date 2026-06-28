from .. import responses
from .base import Action, Outcome


class StatusAction(Action):
    name = "status"
    aliases = ("stat", "stats", "how", "howareyou", "check")

    def run(self, ctx):
        return Outcome(responses.status(ctx.pet))
