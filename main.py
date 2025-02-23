import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import CommandStart
from deep_translator import GoogleTranslator

logging.basicConfig(level=logging.INFO)

TOKEN = "7633655282:AAHLGzqYV7N2qiRt_7qlBsT6vWZ5F4MQdPw"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

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

@dp.message(CommandStart())
async def start_handler(message: Message):
    full_name = message.from_user.full_name
    await message.answer(
        f"Salom, {full_name}\nMenga inglizcha, ruscha matn yuboring, men uni o'zbek tiliga tarjima qilaman. 🇺🇿")


@dp.message()
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


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Bot ishga tushdi 🚀")
    asyncio.run(main())
