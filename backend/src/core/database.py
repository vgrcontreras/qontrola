from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.core.settings import settings
from src.models import User
from src.security import get_password_hash

engine = create_engine(settings.DATABASE_URL)


def init_db(session: Session) -> None:
    superuser_db = session.scalar(
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

        session.add(superuser_db)
        session.commit()
        session.refresh(superuser_db)

    return superuser_db
