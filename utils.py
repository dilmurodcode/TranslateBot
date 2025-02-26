from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.db import db


def get_or_create_user(telegram_id: str, full_name: str):
    filter = {
        "telegram_id": telegram_id
    }
    users = db.get("User", filter)
    if not users:
        fields = {
            "telegram_id": telegram_id,
            "full_name": full_name
        }
        db.create("User", fields)


def get_users():
    users = db.get("User")
    if users:
        return users
    return None



async def get_message_buttons(user_id, bot):
    buttons = []
    try:
        chat = await bot.get_chat(user_id)
        if chat:
            buttons.insert(1, [InlineKeyboardButton(text="👁 Ko‘rish", url=f"tg://user?id={user_id}")])
    except TelegramBadRequest as e:
        print(f"Error getting chat for user_id {user_id}: {e}")

    return InlineKeyboardMarkup(inline_keyboard=buttons)