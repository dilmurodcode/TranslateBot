from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.filters import StateFilter
import asyncio

from utils import send_users_page, send_message_users, get_users

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


class States(StatesGroup):
    picture = State()
    caption = State()

@router.message(F.text == "💌 Fanatlarimga sms")
async def handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if str(user_id) in ["7832158819", "8016755758", '5593831038']:
        await message.answer("Rasm jo'nating")
        await state.set_state(States.picture)
        return


@router.message(StateFilter(States.picture))
async def picture_handler(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Iltimos, rasm jo'nating!")
        await state.clear()
        return

    photo: PhotoSize = message.photo[-1]
    await state.update_data(photo=photo.file_id)
    await message.answer("Endi text yozing")
    await state.set_state(States.caption)


@router.message(StateFilter(States.caption))
async def caption_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if str(user_id) in ["7832158819", "8016755758", '5593831038']:
        data = await state.get_data()
        photo_id = data.get("photo")
        caption = message.text.lstrip('-').strip() if message.text.startswith("--") else message.text
        users = get_users()
        asyncio.create_task(send_message_users(users, message.bot, photo_id, caption))
        await message.answer("Xabar muvaffaqiyatli yuborildi")
        await state.clear()

