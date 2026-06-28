from .. import memory, responses
from .base import Action, Outcome


class TeachAction(Action):
    name = "teach"
    aliases = ("remember", "learn")
    user_cooldown_minutes = 10

    def enabled(self, config):
        return config.enable_teach_command

    def on_disabled(self, ctx):
        return Outcome(responses.teach_disabled(ctx.pet), accepted=False, record=False)

    def run(self, ctx):
        suggestion = memory.submit(ctx.session, ctx.pet, ctx.user, ctx.arg, ctx.config)
        if suggestion is None:
            return Outcome(responses.teach_rejected(ctx.pet), accepted=False, record=False)
        return Outcome(responses.teach_ack(ctx.pet))
