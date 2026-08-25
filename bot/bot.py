import asyncio
from aiogram import Bot, Dispatcher
from config.config import configuration
from bot.handlers.start_handler import router as start_router
from bot.handlers.info_handler import router as info_router

bot = Bot(token=configuration.bot_token.get_secret_value())
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(info_router)

async def main() -> None:
    await dp.start_polling(bot)

try:
    if __name__ == "__main__":
        asyncio.run(main())
except Exception as ex:
    print(f"Возникла ошибка при старте! {ex}")