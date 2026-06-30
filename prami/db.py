import logging
import time
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

log = logging.getLogger("prami.db")


class Base(DeclarativeBase):
    pass


_engine = None
_Session = None


def init_engine(database_url):
    global _engine, _Session

    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    _engine = create_engine(
        database_url,
        future=True,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
    _Session = sessionmaker(bind=_engine, expire_on_commit=False, future=True)
    return _engine


def create_all():
    from . import models  # noqa: F401

    Base.metadata.create_all(_engine)


def wait_for_db(retries=10, delay=3):
    for attempt in range(1, retries + 1):
        try:
            with _engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as exc:
            log.warning("Database not ready (%s/%s): %s", attempt, retries, exc)
            time.sleep(delay)
    raise RuntimeError("Database did not become available")


@contextmanager
def session_scope():
    session = _Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
