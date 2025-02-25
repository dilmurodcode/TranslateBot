import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from deep_translator import GoogleTranslator

from bot.keyboards.admin import keyboards

router = Router()

logging.basicConfig(level=logging.INFO)

translator_en_to_uz = GoogleTranslator(source="en", target="uz")
translator_uz_to_en = GoogleTranslator(source='uz', target='en')
translator_ru_to_uz = GoogleTranslator(source='ru', target='uz')
translator_uz_to_ru = GoogleTranslator(source='uz', target='ru')
translator_en_to_ru = GoogleTranslator(source='en', target='ru')
translator_ru_to_en = GoogleTranslator(source='ru', target='en')


def detect_language(text):
    from googletrans import Translator
    translator = Translator()
    detected = translator.detect(text)
    return detected.lang

@router.message(CommandStart())
async def start_handler(message: Message):
    full_name = message.from_user.full_name
    user_id: int = message.from_user.id
    if str(user_id) in ["7832158819", "8016755758", '5593831038']:
        keyboard = keyboards.admin_keyboard()
        await message.answer("Siz eng zo'risiz tog'a", reply_markup=keyboard)
        return
    await message.answer(
        f"Salom, {full_name} \nMenga inglizcha, ruscha matn yuboring, men uni o'zbek tiliga tarjima qilaman. 🇺🇿")
    return


@router.message(F.text != "👨 Fanatlarim")
async def translate_message(message: Message):
    try:
        text=message.text
        detect  = detect_language(text)
        if detect == 'uz':

            translated_en = translator_uz_to_en.translate(text)
            translated_ru =translator_uz_to_ru.translate(text)
            text = f"""
<b>Ingilizchasi:</b> <i>{translated_en}</i>
<b>Ruscha:</b> <i>{translated_ru}</i>

tarnslated by @dilmurodcode
                        """
            await message.answer(text)

        elif detect == 'en':
            translated_uz = translator_en_to_uz.translate(text)
            translated_ru = translator_en_to_ru.translate(text)
            text = f"""
<b>O'zbekcha:</b> <i>{translated_uz}</i>
<b>Ruscha:</b> <i>{translated_ru}</i>

tarnslated by @dilmurodcode
            """
            await message.answer(text)

        elif detect == 'ru':
            translated_uz = translator_ru_to_uz.translate(text)
            translated_en = translator_ru_to_en.translate(text)
            text = f'''
<b>O'zbekcha:</b> <i>{translated_uz}</i>
<b>Ingilizcha:</b> <i>{translated_en}</i>

tarnslated by @dilmurodcode            
'''
            await message.answer(text)
        else:
            await message.answer(text='Tushunarliroq yozing!!')

    except Exception as e:
        await message.answer("Tarjima vaqtida xatolik yuz berdi! 🔴")
        logging.error(f"Translation error: {e}")

