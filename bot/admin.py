from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from utils import get_users

router = Router()


@router.message(F.text == "👨 Fanatlarim")
async def handler(message: Message):
    user_id = message.from_user.id
    if str(user_id) in ["7832158819", "8016755758", '5593831038']:
        users = get_users()
        await send_users_page(message, users, 0)


async def send_users_page(message: Message, users, page: int):
    per_page = 10
    total_pages = (len(users) + per_page - 1) // per_page
    start = page * per_page
    end = start + per_page
    page_users = users[start:end]

    text = f"Ummumiy soni: {len(users)}\nSahifa: {page + 1}/{total_pages}\n\n"

    buttons = [
        [InlineKeyboardButton(text=user[2] or 'yo‘q', url=f"tg://user?id={user[1]}")]
        for user in page_users
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"users:{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"users:{page + 1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message.reply_to_message:
        await message.reply_to_message.edit_text(text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)


@router.callback_query()
async def pagination_callback(query: CallbackQuery):
    if query.data.startswith("users:"):
        users = get_users()
        page = int(query.data.split(":")[1])
        await send_users_page(query.message, users, page)
        await query.answer()
