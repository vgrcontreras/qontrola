from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.core.settings import settings
from src.models import Tenant, User
from src.security import get_password_hash

engine = create_async_engine(settings.DATABASE_URL)


async def init_db(session: AsyncSession) -> None:
    superuser_db = await session.scalar(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    )

    if not superuser_db:
        # Create a default tenant for the superuser if it doesn't exist
        tenant = await session.scalar(
            select(Tenant).where(Tenant.domain == 'admin.example.com')
        )

        if not tenant:
            tenant = Tenant(name='Admin Tenant', domain='admin.example.com')
            session.add(tenant)
            await session.commit()
            await session.refresh(tenant)

        # Create the superuser with the tenant
        superuser_db = User(
            full_name='admin',
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            tenant_id=tenant.id,
            tenant=tenant,
        )

        session.add(superuser_db)
        await session.commit()
        await session.refresh(superuser_db)

    return superuser_db
