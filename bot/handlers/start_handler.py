import aiohttp
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    telegram_user = message.from_user

    data = {
        "username": telegram_user.username,
        "first_name": telegram_user.first_name,
        "last_name": telegram_user.last_name,
        "telegram_id": telegram_user.id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/user/register",
            json=data
        ) as response:
            res = await response.json()
    await message.answer(f"Привет {telegram_user.first_name} я бот")