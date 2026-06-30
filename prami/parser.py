import re
from dataclasses import dataclass
from html import unescape

from .actions.registry import REGISTRY

_ALIAS_TO_COMMAND = REGISTRY.alias_map()
PHRASE_ALIASES = REGISTRY.phrase_map()

_MENTION = re.compile(r"@[\w.\-]+(?:@[\w.\-]+)?")
_WHITESPACE = re.compile(r"\s+")


@dataclass
class Parsed:
    name: str | None
    arg: str = ""


def strip_html(content):
    text = re.sub(r"(?i)<br\s*/?>", " ", content)
    text = re.sub(r"(?i)</p>", " ", text)
    text = re.sub(r"<[^>]+>", "", text)
    return unescape(text)


def _after(raw, keyword):
    match = re.search(r"\b" + re.escape(keyword) + r"\b", raw, re.IGNORECASE)
    return raw[match.end():].strip() if match else ""


def parse(content):
    raw = _WHITESPACE.sub(" ", strip_html(content)).strip()
    detect = _WHITESPACE.sub(" ", _MENTION.sub(" ", raw)).strip().lower()

    for phrase, command in PHRASE_ALIASES.items():
        if detect.startswith(phrase):
            return Parsed(command, _after(raw, phrase))

    for token in detect.split():
        command = _ALIAS_TO_COMMAND.get(token)
        if command:
            return Parsed(command, _after(raw, token))

    return Parsed(None)


def parse_command(content):
    return parse(content).name