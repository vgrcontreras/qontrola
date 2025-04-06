from unittest.mock import AsyncMock, patch

import pytest

from src.initial_data import init, main


@pytest.mark.asyncio
async def test_init():
    """Test the init function calls init_db with the correct session"""
    mock_session = AsyncMock()
    mock_init_db = AsyncMock()

    # Create a context manager mock that returns our mock session
    enter_mock = AsyncMock()
    enter_mock.__aenter__.return_value = mock_session

    with (
        patch(
            'src.initial_data.AsyncSession', return_value=enter_mock
        ) as mock_async_session,
        patch('src.initial_data.init_db', mock_init_db),
    ):
        # Call the function we're testing
        await init()

        # Verify the session was created with the correct engine
        from src.initial_data import engine  # noqa

        mock_async_session.assert_called_once_with(engine)

        # Verify init_db was called with our mock session
        mock_init_db.assert_called_once_with(mock_session)


@pytest.mark.asyncio
async def test_main():
    """Test the main function calls init"""
    with patch('src.initial_data.init', AsyncMock()) as mock_init:
        await main()
        mock_init.assert_called_once()
