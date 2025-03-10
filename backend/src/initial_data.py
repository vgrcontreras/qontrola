from loguru import logger
from sqlalchemy.orm import Session

from src.core.database import engine, init_db


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info('Creating initial data')
    init()
    logger.info('Initial data created')


if __name__ == '__main__':
    main()
