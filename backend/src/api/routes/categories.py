"""API routes for categories."""

from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.api.dependencies import CurrentUser, T_Session
from src.models import Category
from src.schemas.base import Message
from src.schemas.categories import (
    CategoryCreate,
    CategoryList,
    CategoryResponse,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=CategoryResponse,
)
async def create_category(
    session: T_Session,
    category: CategoryCreate,
    current_user: CurrentUser,
) -> Category:
    """Create a new category."""
    # Check if category exists with the same name
    normalized_name = category.name.strip()
    category_db = await session.scalar(
        select(Category).where(Category.name == normalized_name)
    )

    if category_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Category already exists',
        )

    # Create the category
    category_db = Category(
        name=normalized_name,
    )

    session.add(category_db)
    await session.commit()
    await session.refresh(category_db)

    return category_db


@router.get(
    path='/{category_id}',
    status_code=HTTPStatus.OK,
    response_model=CategoryResponse,
)
async def read_category_by_id(
    session: T_Session,
    category_id: UUID,
    current_user: CurrentUser,
) -> Category:
    """
    Get a specific category.
    """
    query = select(Category).where(Category.id == category_id)

    category_db = await session.scalar(query)

    if not category_db:
        raise HTTPException(
            detail="Category doesn't exist", status_code=HTTPStatus.NOT_FOUND
        )

    return category_db


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=CategoryList,
)
async def read_all_categories(
    session: T_Session,
    current_user: CurrentUser,
) -> dict:
    """
    Get all categories.
    """
    query = select(Category).where(
        Category.is_active == True,  # noqa: E712
    )

    categories_db = await session.scalars(query)

    return {'categories': categories_db.all()}


@router.delete(
    path='/{category_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
async def delete_category(
    session: T_Session,
    category_id: UUID,
    current_user: CurrentUser,
) -> dict:
    """
    Delete (deactivate) a category.
    """
    category_db = await session.scalar(
        select(Category).where(Category.id == category_id)
    )

    if not category_db:
        raise HTTPException(
            detail="Category doesn't exist", status_code=HTTPStatus.NOT_FOUND
        )

    category_db.is_active = False

    session.add(category_db)
    await session.commit()

    return {'message': 'Category deleted'}
