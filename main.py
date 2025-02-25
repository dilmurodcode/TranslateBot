import asyncio

from aiogram import Bot, Dispatcher, Router

from bot.middlewares import CreateOrGetUserMiddleware
from bot.translate import router as translate_router
from bot.admin import router as admin_router
from aiogram.client.default import DefaultBotProperties

router = Router()
router.include_router(translate_router)
router.include_router(admin_router)


async def main():
    TOKEN = "7633655282:AAHLGzqYV7N2qiRt_7qlBsT6vWZ5F4MQdPw"
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_router(router)

    dp.message.middleware(CreateOrGetUserMiddleware())
    dp.callback_query.middleware(CreateOrGetUserMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot ishga tushdi 🚀")
    asyncio.run(main())
