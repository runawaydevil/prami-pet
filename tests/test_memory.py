from prami import engine, memory, sanitize


def test_clean_memory_strips_quotes_and_html():
    assert sanitize.clean_memory('"<b>Soup is a weather condition.</b>"') == "Soup is a weather condition."


def test_clean_memory_rejects_url_and_mention():
    assert sanitize.clean_memory("visit http://x.example") is None
    assert sanitize.clean_memory("ask @bob") is None


def test_clean_memory_truncates():
    assert len(sanitize.clean_memory("x" * 300, max_len=180)) == 180


def test_categorize():
    assert memory.categorize("Prami is afraid of silent printers") == "fear"
    assert memory.categorize("Prami believes soup is a weather condition") == "lore"
    assert memory.categorize("Prami likes warm blankets") == "preference"


def test_submit_and_approve_flow(session, pet, user, config):
    suggestion = memory.submit(session, pet, user, "Prami believes soup is weather.", config)
    assert suggestion.status == "pending"
    assert memory.by_status(session, "pending") == [suggestion]
    memory.approve(session, suggestion.id, "admin")
    assert suggestion.status == "approved"
    assert memory.by_status(session, "approved") == [suggestion]


def test_reject_records_reason(session, pet, user, config):
    suggestion = memory.submit(session, pet, user, "something forgettable", config)
    memory.reject(session, suggestion.id, "admin", "spam")
    assert suggestion.status == "rejected"
    assert suggestion.rejection_reason == "spam"


def test_approve_nonpending_returns_none(session, pet, user, config):
    suggestion = memory.submit(session, pet, user, "x", config)
    memory.approve(session, suggestion.id, "admin")
    assert memory.approve(session, suggestion.id, "admin") is None


def test_teach_disabled_by_default(session, pet, user, config):
    result = engine.handle(session, pet, user, "teach", config, arg="Prami fears printers")
    assert result.accepted is False
    assert memory.by_status(session, "pending") == []


def test_teach_creates_pending_when_enabled(session, pet, user, config):
    config.enable_teach_command = True
    result = engine.handle(session, pet, user, "teach", config, arg="Prami fears printers")
    assert result.accepted is True
    assert len(memory.by_status(session, "pending")) == 1


def test_teach_rejects_invalid_content(session, pet, user, config):
    config.enable_teach_command = True
    result = engine.handle(session, pet, user, "teach", config, arg="see http://x.example")
    assert result.accepted is False
    assert memory.by_status(session, "pending") == []
