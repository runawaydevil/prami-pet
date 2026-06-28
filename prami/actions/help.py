from .. import responses
from .base import Action, Outcome


class HelpAction(Action):
    name = "help"
    aliases = ("commands", "menu", "?")

    def run(self, ctx):
        return Outcome(responses.help_text(ctx.config))
