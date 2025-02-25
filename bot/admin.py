from aiogram import Router, F
from aiogram.types import Message

from utils import get_users
router = Router()

@router.message(F.text == "👨 Fanatlarim")
async def handler(message: Message):
    user_id = message.from_user.id
    if str(user_id) in ["7832158819", "8016755758", '5593831038']:
        users = get_users()
        text = ""
        for user in users:
            text += f"Id: {user[0]} Ism: {user[2] or "yo'q"}, Telegram ID: {user[1] or 0} \n\n"

        text += f"Ummumiy soni: {len(users)}"
        await message.answer(text)
        return



