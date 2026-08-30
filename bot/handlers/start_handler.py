import aiohttp
import os
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from bot.keyboard.keyboard import hello_button, info_button

router = Router()

load_dotenv()
API_URL = os.getenv("API_URL")

@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(
        "🍳 Добро пожаловать!\n\n"
        "Это ваш помощник по питанию, экономии и полезным цифровым материалам.\n\n"
        "📚 Покупать полезные материалы\n"
        "— меню для похудения на неделю\n"
        "— советы по экономии на ЖКХ\n"
        "— материалы по раскладам Таро\n\n"
        "🍳 Получать рецепты по фото\n"
        "Просто отправьте фотографию холодильника или продуктов — \n"
        "AI определит продукты и предложит подходящие рецепты.\n\n"
        "🎁 Бесплатно\n"
        "До 2 запросов по фото в день — без оплаты.\n\n"
        "Нажмите «Начать», чтобы зарегистрироваться и получить доступ к возможностям бота.",
        reply_markup=hello_button
    )

@router.callback_query(F.data == "button_hello")
async def start_bot(callback: CallbackQuery):
    await callback.answer()

    telegram_user = callback.from_user

    data = {
        "username": telegram_user.username,
        "first_name": telegram_user.first_name,
        "last_name": telegram_user.last_name,
        "telegram_id": telegram_user.id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/user/register",
            json=data
        ) as response:
            res = await response.json()

    await callback.message.answer(f"Привет {telegram_user.first_name}", reply_markup=info_button)

