from .. import responses, sanitize
from .base import Action, Outcome


class NicknameAction(Action):
    name = "nickname"
    aliases = ("nick",)
    phrase_aliases = ("name me", "call me")
    user_cooldown_minutes = 5

    def run(self, ctx):
        arg = ctx.arg.strip()
        if arg.lower() == "clear":
            ctx.user.nickname = None
            return Outcome(responses.nickname_cleared(ctx.pet), address=False)

        cleaned = sanitize.clean_nickname(arg)
        if not cleaned:
            return Outcome(responses.nickname_rejected(ctx.pet), accepted=False, record=False, address=False)

        ctx.user.nickname = cleaned
        return Outcome(responses.nickname_set(ctx.pet, cleaned), address=False)
