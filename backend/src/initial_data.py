from asyncio import run

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import engine, init_db


async def init() -> None:
    async with AsyncSession(engine) as session:
        await init_db(session)


async def main() -> None:
    logger.info('Creating initial data')
    await init()
    logger.info('Initial data created')


if __name__ == '__main__':
    run(main())
