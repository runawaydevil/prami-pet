class ActionRegistry:
    def __init__(self):
        self._by_name = {}
        self._by_alias = {}
        self._phrases = {}

    def register(self, action):
        self._by_name[action.name] = action
        for alias in (action.name, *action.aliases):
            self._by_alias[alias.lower()] = action.name
        for phrase in action.phrase_aliases:
            self._phrases[phrase.lower()] = action.name

    def resolve(self, command):
        return self._by_name.get(command) or self._by_name["unknown"]

    def canonical(self, token):
        return self._by_alias.get((token or "").lower())

    def alias_map(self):
        return dict(self._by_alias)

    def phrase_map(self):
        return dict(self._phrases)

    def is_enabled(self, command, config):
        action = self._by_name.get(command)
        return bool(action and action.enabled(config))

    def names(self):
        return list(self._by_name)


def build_registry():
    from .admin import AdminAction
    from .care import CleanAction, FeedAction, PetAction, PlayAction, SleepAction, WakeAction
    from .events import EventAction, EventHelpAction, VoteAction
    from .help import HelpAction
    from .nickname import NicknameAction
    from .status import StatusAction
    from .teach import TeachAction
    from .unknown import UnknownAction

    registry = ActionRegistry()
    actions = (
        StatusAction, HelpAction, UnknownAction,
        FeedAction, PlayAction, PetAction, CleanAction, SleepAction, WakeAction,
        NicknameAction, TeachAction,
        EventAction, EventHelpAction, VoteAction,
        AdminAction,
    )
    for action_cls in actions:
        registry.register(action_cls())
    return registry


REGISTRY = build_registry()
