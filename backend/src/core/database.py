from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.core.settings import settings
from src.models import User
from src.security import get_password_hash

engine = create_async_engine(settings.DATABASE_URL)


async def init_db(session: AsyncSession) -> None:
    superuser_db = await session.scalar(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    )

    if not superuser_db:
        superuser_db = User(
            first_name='admin',
            last_name='admin',
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            salary=0,
            is_superuser=True,
        )

        await session.add(superuser_db)
        await session.commit()
        await session.refresh(superuser_db)

    return superuser_db
