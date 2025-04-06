import uuid
from datetime import date, datetime
from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class IdentifierType(str, Enum):
    cpf = 'cpf'
    cnpj = 'cnpj'


@table_registry.mapped_as_dataclass
class Tenant:
    __tablename__ = 'tenants'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(nullable=False)
    domain: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True, init=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )
    users: Mapped[List['User']] = relationship(
        back_populates='tenant',
        cascade='all, delete-orphan',
        init=False,
        default_factory=list,
    )
    clients: Mapped[List['Client']] = relationship(
        back_populates='tenant',
        cascade='all, delete-orphan',
        init=False,
        default_factory=list,
    )
    projects: Mapped[List['Project']] = relationship(
        back_populates='tenant',
        cascade='all, delete-orphan',
        init=False,
        default_factory=list,
    )


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    # Tenant relationship
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    tenant: Mapped['Tenant'] = relationship(back_populates='users')
    full_name: Mapped[str] = mapped_column(default=None, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )


@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = 'clients'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str]
    client_type: Mapped[str]
    type_identifier: Mapped[IdentifierType]
    identifier: Mapped[str] = mapped_column(unique=True)
    # Tenant relationship
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    tenant: Mapped['Tenant'] = relationship(back_populates='clients')
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )
    updated_by: Mapped[datetime] = mapped_column(default=None, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)


@table_registry.mapped_as_dataclass
class Project:
    __tablename__ = 'projects'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(unique=True)
    status_state: Mapped[str] = mapped_column(nullable=True)
    project_value: Mapped[float] = mapped_column(nullable=True)
    target_date: Mapped[date] = mapped_column(nullable=True)
    # Tenant relationship
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    tenant: Mapped['Tenant'] = relationship(back_populates='projects')
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )
    updated_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=None, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)
