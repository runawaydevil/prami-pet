from prami import templates


def test_every_command_pool_is_well_formed():
    for command, variants in templates.COMMAND_TEMPLATES.items():
        assert "normal" in variants, f"{command} is missing a normal variant"
        for variant, pool in variants.items():
            assert pool, f"{command}/{variant} is empty"
            assert all(isinstance(line, str) and line.strip() for line in pool)


def test_autopost_pools_are_non_empty():
    for group, pool in templates.AUTOPOST.items():
        assert pool, f"autopost/{group} is empty"


def test_event_scenarios_are_well_formed():
    keys = set()
    for scenario in templates.EVENT_SCENARIOS:
        assert scenario["key"] and scenario["key"] not in keys
        keys.add(scenario["key"])
        assert scenario["title"] and scenario["description"]
        assert scenario["options"]
        for option in scenario["options"].values():
            assert option["label"] and option["text"]
            assert isinstance(option["deltas"], dict)
