from prami import autopost, events, memory


def test_compose_sets_last_category(session, pet, config):
    text = autopost.compose(session, pet, config)
    assert text
    assert pet.last_autopost_category is not None


def test_compose_avoids_immediate_repeat(session, pet, config):
    seen = set()
    for _ in range(8):
        autopost.compose(session, pet, config)
        seen.add(pet.last_autopost_category)
    assert len(seen) > 1


def test_active_event_reminder_is_reachable(session, pet, config):
    config.enable_events = True
    template = next(t for t in events.TEMPLATES if t["key"] == "egg")
    events.start(session, pet, config, template=template)
    seen = set()
    for _ in range(60):
        pet.last_autopost_category = None
        autopost.compose(session, pet, config)
        seen.add(pet.last_autopost_category)
    assert "active_event_reminder" in seen


def test_approved_memory_callback_is_reachable(session, pet, user, config):
    suggestion = memory.submit(session, pet, user, "soup is a weather condition", config)
    memory.approve(session, suggestion.id, "admin")
    seen = set()
    for _ in range(80):
        pet.last_autopost_category = None
        autopost.compose(session, pet, config)
        seen.add(pet.last_autopost_category)
    assert "approved_memory_callback" in seen
