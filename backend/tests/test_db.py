from dataclasses import asdict
from uuid import UUID

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

    department_dict = asdict(department_db)

    assert isinstance(department_dict['id'], UUID)
    assert department_dict['name'] == 'test_department'
    assert department_dict['created_at'] == time
    assert department_dict['updated_at'] == time
