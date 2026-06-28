import logging

import prami
from .app import Poller, bootstrap
from .config import config
from .scheduler import build_scheduler


def main():
    logging.basicConfig(
        level=config.log_level.upper(),
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("apscheduler").setLevel(logging.WARNING)

    log = logging.getLogger("prami")
    log.info("Starting Prami %s", prami.__version__)

    client = bootstrap()
    scheduler = build_scheduler(client)
    scheduler.start()

    try:
        Poller(client).run()
    except KeyboardInterrupt:
        log.info("Shutting down, see you soon")
    finally:
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    main()
