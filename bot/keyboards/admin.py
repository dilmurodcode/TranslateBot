from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class Keyboards:

    @staticmethod
    def admin_keyboard():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👨 Fanatlarim")]
            ], resize_keyboard=True
        )


keyboards = Keyboards()




