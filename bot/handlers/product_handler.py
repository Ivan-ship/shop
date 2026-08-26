import os
import aiohttp
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


router = Router()

load_dotenv()

API_URL = os.getenv("API_URL")

@router.callback_query(F.data == "button_catalog")
async def get_product(callback: CallbackQuery):
    await callback.answer()

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_URL}/products"
        ) as response:
            if response.status != 200:
                await callback.message.answer(
                    "Не удалось получить товары"
                )
                return
            products = await response.json()

    prod_keyboard = []

    for product in products:
        prod_keyboard.append([
            InlineKeyboardButton(
                text=f"{product['name']}- {product['price']} ₽",
                callback_data=f"product:{product['prod_id']}"
            )
        ])
        markup = InlineKeyboardMarkup(
            inline_keyboard=prod_keyboard
        )
        await callback.message.edit_text(
            text="Доступные товары",
            reply_markup=markup
        )
