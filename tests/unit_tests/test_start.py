import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types

from src.bot.handlers.start import (
    start_handler,
    back_to_menu_handler,
    send_main_menu,
)


class TestStartHandlers:
    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.fixture
    def fake_message(self):
        msg = MagicMock(spec=types.Message)
        msg.from_user = MagicMock(spec=types.User, id=123, username="test_user")
        msg.answer = AsyncMock()
        return msg

    @pytest.fixture
    def fake_callback(self):
        cb = MagicMock(spec=types.CallbackQuery)
        cb.message = MagicMock()
        cb.message.answer = AsyncMock()
        cb.answer = AsyncMock()
        return cb


    @pytest.mark.asyncio
    async def test_start_handler_success(self, fake_message, mock_db):
        with (
            patch("src.bot.handlers.start.send_main_menu", new_callable=AsyncMock) as mock_menu,
            patch("src.bot.handlers.start.UserService") as MockUserService,
        ):
            mock_service = MockUserService.return_value
            mock_service.upsert_from_tg = AsyncMock()

            await start_handler(fake_message, mock_db)

            mock_menu.assert_awaited_once_with(fake_message)
            MockUserService.assert_called_once_with(mock_db)
            mock_service.upsert_from_tg.assert_awaited_once_with(fake_message.from_user)


    @pytest.mark.asyncio
    async def test_start_handler_without_user(self, fake_message, mock_db):
        fake_message.from_user = None
        with (
            patch("src.bot.handlers.start.send_main_menu", new_callable=AsyncMock) as mock_menu,
            patch("src.bot.handlers.start.UserService") as MockUserService,
        ):
            await start_handler(fake_message, mock_db)

            mock_menu.assert_awaited_once_with(fake_message)
            MockUserService.assert_not_called()


    @pytest.mark.asyncio
    async def test_back_to_menu_handler(self, fake_callback):
        with patch("src.bot.handlers.start.send_main_menu", new_callable=AsyncMock) as mock_menu:
            await back_to_menu_handler(fake_callback)

            mock_menu.assert_awaited_once_with(fake_callback)


    @pytest.mark.asyncio
    async def test_send_main_menu_with_message(self, fake_message):
        await send_main_menu(fake_message)

        fake_message.answer.assert_awaited_once()
        assert "Добро пожаловать" in fake_message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_send_main_menu_with_callback(self, fake_callback):
        await send_main_menu(fake_callback)

        fake_callback.message.answer.assert_awaited_once()
        fake_callback.answer.assert_awaited_once()