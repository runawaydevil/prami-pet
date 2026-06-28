from .. import events as events_mod
from .. import responses
from .base import Action, Outcome


class EventAction(Action):
    name = "event"

    def run(self, ctx):
        event = events_mod.active(ctx.session, ctx.now)
        if event is None:
            return Outcome(responses.no_event(ctx.pet), record=False)
        text = responses.event_show(ctx.pet, event.title, event.description, events_mod.options_text(event))
        return Outcome(text, record=False)


class EventHelpAction(Action):
    name = "helpevent"
    aliases = ("help-event",)

    def run(self, ctx):
        event = events_mod.active(ctx.session, ctx.now)
        if event is None:
            return Outcome(responses.no_event(ctx.pet), record=False)
        text = responses.event_help(ctx.pet, event.title, events_mod.options_text(event))
        return Outcome(text, record=False)


class VoteAction(Action):
    name = "vote"

    def run(self, ctx):
        event = events_mod.active(ctx.session, ctx.now)
        if event is None:
            return Outcome(responses.no_event(ctx.pet), accepted=False, record=False)
        ok, reason = events_mod.vote(ctx.session, event, ctx.user, ctx.arg)
        if not ok:
            text = responses.vote_rejected(ctx.pet, reason, events_mod.options_text(event))
            return Outcome(text, accepted=False, record=False)
        return Outcome(responses.vote_ack(ctx.pet, event.title))
