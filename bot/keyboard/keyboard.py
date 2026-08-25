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


info_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📚 Товары",
                callback_data="button_catalog"
            ),
            InlineKeyboardButton(
                text="🍳 Рецепты по фото",
                callback_data="button_recipe"
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ О проекте",
                callback_data="about_project"
            ),
            InlineKeyboardButton(
                text="📞 Поддержка",
                url = "https://github.com/Ivan-ship"
            )
        ]
    ]
)