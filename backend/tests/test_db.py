from dataclasses import asdict
from uuid import UUID

import pytest
from sqlalchemy import select

from src.models import Tenant


@pytest.mark.asyncio
async def test_create_tenant_db(session, mock_db_time):
    with mock_db_time(model=Tenant) as time:
        new_tenant = Tenant(name='test_tenant', domain='test-domain.com')

        session.add(new_tenant)
        await session.commit()

    tenant_db = await session.scalar(
        select(Tenant).where(Tenant.name == 'test_tenant')
    )

    tenant_dict = asdict(tenant_db)

    assert isinstance(tenant_dict['id'], UUID)
    assert tenant_dict['name'] == 'test_tenant'
    assert tenant_dict['domain'] == 'test-domain.com'
    assert tenant_dict['created_at'] == time
    assert tenant_dict['updated_at'] == time
