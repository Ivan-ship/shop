from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Hello button
hello_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✋ Начать",
                style="primary",
                callback_data="button_hello"
            )
        ]
    ]
)


gds_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📚 Товары",
                callback_data="button_goods"
            )
        ]
    ]
)