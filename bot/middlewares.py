from typing import Callable, Any, Awaitable, Dict

import aiogram
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils import get_or_create_user


class CreateOrGetUserMiddleware(aiogram.BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery | FSMContext,
            data: Dict[str, Any]
    ) -> Any:
        get_or_create_user(str(event.from_user.id), str(event.from_user.full_name))
        return await handler(event, data)






