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


def user_id_is_accessible(user_id: int) -> bool:
    try:
        InlineKeyboardButton(text="Test", url=f"tg://user?id={user_id}")
        return True
    except TelegramBadRequest:
        return False


sync


def send_users_page(page: int = 0):
    users = get_users()
    per_page = 10
    total_pages = (len(users) + per_page - 1) // per_page
    start = page * per_page
    end = start + per_page
    page_users = users[start:end]

    text = f"Umumiy soni: {len(users)}\n\n"

    buttons = []

    for user in page_users:
        user_name = user[2] or 'yo‘q'
        user_id = user[1]

        if user_id_is_accessible(user_id):
            button = InlineKeyboardButton(text=user_name, url=f"tg://user?id={user_id}")
        else:
            button = InlineKeyboardButton(text=f"{user_name} (Mavjud emas)", callback_data="none")

        buttons.append([button])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"users:{page - 1}"))

    nav_buttons.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="none"))

    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"users:{page + 1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return text, keyboard