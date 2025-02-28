from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class Keyboards:

    @staticmethod
    def admin_keyboard():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👨 Fanatlarim")],
                [KeyboardButton(text="💌 Fanatlarimga sms")]
            ], resize_keyboard=True
        )


keyboards = Keyboards()




