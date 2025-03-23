from dataclasses import asdict

import pytest
from sqlalchemy import select

from src.models import Department


@pytest.mark.asyncio
async def test_create_department_db(session, mock_db_time):
    with mock_db_time(model=Department) as time:
        new_department = Department(name='test_department')

        session.add(new_department)
        await session.commit()

    department_db = await session.scalar(
        select(Department).where(Department.name == 'test_department')
    )

    assert asdict(department_db) == {
        'id': 1,
        'name': 'test_department',
        'created_at': time,
        'updated_at': time,
    }
