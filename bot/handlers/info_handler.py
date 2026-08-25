from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboard.keyboard import info_button


router = Router()

#About project
@router.callback_query(F.data == "about_project")
async def about_proj(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Developer Ivan"
    )