import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class IdentifierType(str, Enum):
    cpf = 'cpf'
    cnpj = 'cnpj'


@table_registry.mapped_as_dataclass
class Category:
    __tablename__ = 'categories'

    # Fields without default values first
    name: Mapped[str] = mapped_column(nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    tenant: Mapped['Tenant'] = relationship(
        back_populates='categories', init=False
    )

    # Fields with defaults or init=False after
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships with default factory
    projects: Mapped[List['Project']] = relationship(
        back_populates='category',
        init=False,
        default_factory=list,
    )
    tasks: Mapped[List['Task']] = relationship(
        back_populates='category',
        init=False,
        default_factory=list,
    )

    # Add unique constraint for category name per tenant
    __table_args__ = (
        UniqueConstraint(
            'name', 'tenant_id', name='uq_category_name_per_tenant'
        ),
    )


@table_registry.mapped_as_dataclass
class Tenant:
    __tablename__ = 'tenants'

    # Fields without default values first
    name: Mapped[str] = mapped_column(nullable=False)
    domain: Mapped[str] = mapped_column(nullable=False, unique=True)

    # Fields with defaults after
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    is_active: Mapped[bool] = mapped_column(default=True, init=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )

    # Relationships initialized with defaults
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
    tasks: Mapped[List['Task']] = relationship(
        back_populates='tenant',
        cascade='all, delete-orphan',
        init=False,
        default_factory=list,
    )
    categories: Mapped[List['Category']] = relationship(
        back_populates='tenant',
        cascade='all, delete-orphan',
        init=False,
        default_factory=list,
    )


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    # Fields without default values first
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    tenant: Mapped['Tenant'] = relationship(back_populates='users')

    # Fields with defaults after
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    full_name: Mapped[Optional[str]] = mapped_column(
        default=None, nullable=True
    )
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

    # Fields without default values first
    name: Mapped[str]
    client_type: Mapped[str]
    type_identifier: Mapped[IdentifierType]
    identifier: Mapped[str] = mapped_column()
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    tenant: Mapped['Tenant'] = relationship(back_populates='clients')

    # Fields with defaults after
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )
    updated_by: Mapped[Optional[datetime]] = mapped_column(
        default=None, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    # Add composite unique constraint for identifier per tenant
    __table_args__ = (
        UniqueConstraint(
            'identifier', 'tenant_id', name='uix_client_identifier_tenant'
        ),
    )


@table_registry.mapped_as_dataclass
class Project:
    __tablename__ = 'projects'

    # Fields without default values must come first
    name: Mapped[str] = mapped_column()
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    tenant: Mapped['Tenant'] = relationship(
        back_populates='projects', init=False
    )

    # Fields with defaults or init=False can come after
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('categories.id'),
        nullable=True,
        default=None,
    )
    category: Mapped[Optional['Category']] = relationship(
        back_populates='projects', init=False
    )
    status_state: Mapped[Optional[str]] = mapped_column(
        nullable=True, default=None
    )
    project_value: Mapped[Optional[float]] = mapped_column(
        nullable=True, default=None
    )
    target_date: Mapped[Optional[date]] = mapped_column(
        nullable=True, default=None
    )
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), default=None, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships with default factory
    tasks: Mapped[List['Task']] = relationship(
        back_populates='project',
        cascade='all, delete-orphan',
        init=False,
        default_factory=list,
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )

    # Add composite unique constraint for project name per tenant
    __table_args__ = (
        UniqueConstraint('name', 'tenant_id', name='uix_project_name_tenant'),
    )


@table_registry.mapped_as_dataclass
class Task:
    __tablename__ = 'tasks'

    # Required fields without defaults
    title: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    project: Mapped['Project'] = relationship(
        back_populates='tasks', init=False
    )
    tenant: Mapped['Tenant'] = relationship(back_populates='tasks', init=False)

    # Fields with defaults or init=False
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('categories.id'),
        nullable=True,
        default=None,
    )
    category: Mapped[Optional['Category']] = relationship(
        back_populates='tasks', init=False
    )
    description: Mapped[Optional[str]] = mapped_column(
        nullable=True, default=None
    )
    status: Mapped[str] = mapped_column(nullable=False, default='to_do')
    priority: Mapped[str] = mapped_column(nullable=False, default='medium')
    due_date: Mapped[Optional[date]] = mapped_column(
        nullable=True, default=None
    )
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), default=None, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )
