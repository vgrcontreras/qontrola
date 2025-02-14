from sqlalchemy import select

from backend.models import Department


def test_create_department_db(session):
    new_department = Department(name='test_department')

    session.add(new_department)
    session.commit()
    session.refresh(new_department)

    department_db = session.scalar(
        select(Department).where(Department.name == 'test_department')
    )

    assert department_db.name == 'test_department'
