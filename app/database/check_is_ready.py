import logging

from fastapi import Depends
from sqlalchemy.orm import Session  # type: ignore
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.dependencies.database_connection import get_database_connection
from app.logger import logger

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db_conn = Depends(get_database_connection)
        db = Session(bind=db_conn)
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
