import os
import aiohttp
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery,
    BufferedInputFile
)


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

@router.callback_query(F.data.startswith("product:"))
async def get_product_pdf(callback: CallbackQuery):
    await callback.answer()

    prod_id = int(callback.data.split(":")[1])

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/products/{prod_id}/payment",
            json={
                "telegram_id": callback.from_user.id
            }
        ) as response:
            if response.status != 200:
                text = await response.text()

                await callback.answer(
                    "Не удалось создать платеж"
                )
                return

            payment = await response.json()

        payment_url = payment["payment_url"]

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💳 Оплатить",
                        url=payment_url
                    )
                ]
            ]
        )

            pdf_data = await response.read()
    
    await callback.message.answer_document(
        document = BufferedInputFile(
            pdf_data,
            filename=f"product_{prod_id}.pdf"
        )
    )