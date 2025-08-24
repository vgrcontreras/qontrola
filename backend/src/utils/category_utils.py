"""Utility functions for category management."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category


async def get_or_create_category(
    db: AsyncSession, category_name: str
) -> Optional[Category]:
    """
    Get or create a category with the given name.

    Args:
        db: Database session
        category_name: Name of the category to retrieve or create

    Returns:
        The retrieved or newly created category
    """
    if not category_name:
        return None

    # Strip spaces to avoid duplicates with extra whitespace
    normalized_name = category_name.strip()

    # Try to find existing category
    query = select(Category).where(
        Category.name == normalized_name,
        Category.is_active == True,  # noqa: E712
    )

    category = await db.scalar(query)

    # If category exists, return it
    if category:
        return category

    # Otherwise, create a new category
    new_category = Category(
        name=normalized_name,
    )

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category
