from prami import social


def test_favourite_worthy_feed_when_starving():
    assert social.favourite_worthy("feed", {"hunger": 90, "social": 50, "cleanliness": 70}, None) is True
    assert social.favourite_worthy("feed", {"hunger": 50, "social": 50, "cleanliness": 70}, None) is False


def test_favourite_worthy_pet_when_lonely():
    assert social.favourite_worthy("pet", {"hunger": 40, "social": 10, "cleanliness": 70}, None) is True


def test_favourite_worthy_clean_when_filthy():
    assert social.favourite_worthy("clean", {"hunger": 40, "social": 50, "cleanliness": 10}, None) is True


def test_favourite_not_worthy_for_ordinary_play():
    assert social.favourite_worthy("play", {"hunger": 40, "social": 50, "cleanliness": 70}, None) is False


def test_boost_worthy_only_on_critical_save():
    assert social.boost_worthy(True, False) is True
    assert social.boost_worthy(False, False) is False
    assert social.boost_worthy(True, True) is False
