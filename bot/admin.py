from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from utils import send_users_page

router = Router()


@router.message(F.text == "👨 Fanatlarim")
async def handler(message: Message):
    user_id = message.from_user.id
    if str(user_id) in ["7832158819", "8016755758", '5593831038']:
        text, keyboard = await send_users_page(message.bot)
        await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("users:"))
async def pagination(c: CallbackQuery):
    page = int(c.data.split(":")[1])
    text, keyboard = await send_users_page(c.bot, page)
    await c.message.edit_text(text, reply_markup=keyboard)
