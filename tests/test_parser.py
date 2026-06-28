import pytest

from prami.parser import parse, parse_command, strip_html


@pytest.mark.parametrize(
    "content,expected",
    [
        ("<p>@prami feed</p>", "feed"),
        ("<p>@prami@instance.social PLAY now please</p>", "play"),
        ("@prami status", "status"),
        ("<p>hey @prami can you <b>eat</b> something</p>", "feed"),
        ("@prami pat the creature", "pet"),
        ("@prami WAKE UP", "wake"),
        ("@prami help", "help"),
        ("@prami ?", "help"),
    ],
)
def test_recognized_commands(content, expected):
    assert parse_command(content) == expected


def test_unknown_command_returns_none():
    assert parse_command("<p>@prami good morning friend</p>") is None


def test_first_command_wins():
    assert parse_command("@prami feed and then play") == "feed"


def test_strip_html_unescapes_and_drops_tags():
    assert strip_html("<p>tom &amp; jerry</p>").strip() == "tom & jerry"


def test_mentions_are_not_read_as_commands():
    assert parse_command("@feed @prami pet") == "pet"


def test_empty_content_is_none():
    assert parse_command("") is None


def test_parse_nickname_with_argument():
    result = parse("<p>@prami nickname Soup Wizard</p>")
    assert result.name == "nickname"
    assert result.arg == "Soup Wizard"


def test_parse_call_me_phrase():
    result = parse("@prami call me Soup")
    assert result.name == "nickname"
    assert result.arg == "Soup"


def test_parse_name_me_phrase():
    result = parse("@prami name me Captain")
    assert (result.name, result.arg) == ("nickname", "Captain")


def test_parse_nickname_clear():
    result = parse("@prami nickname clear")
    assert (result.name, result.arg) == ("nickname", "clear")


def test_parse_plain_command_has_empty_arg():
    result = parse("@prami feed")
    assert (result.name, result.arg) == ("feed", "")
