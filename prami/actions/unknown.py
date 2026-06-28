from .. import responses
from .base import Action, Outcome


class UnknownAction(Action):
    name = "unknown"

    def run(self, ctx):
        return Outcome(responses.unknown(ctx.pet))
