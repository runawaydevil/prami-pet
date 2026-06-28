import pytest

from prami import repository as repo
from prami.config import Config
from prami.db import create_all, init_engine, session_scope


@pytest.fixture
def config():
    cfg = Config()
    cfg.database_url = "sqlite:///:memory:"
    cfg.max_per_user_hour = 100
    cfg.max_global_hour = 1000
    cfg.default_visibility = "unlisted"
    return cfg


@pytest.fixture
def session(config):
    init_engine(config.database_url)
    create_all()
    with session_scope() as s:
        yield s


@pytest.fixture
def pet(session, config):
    return repo.get_or_create_pet(session, config)


@pytest.fixture
def user(session):
    return repo.get_or_create_user(session, "tester@example.social", mastodon_id="1")
