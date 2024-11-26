from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📜 TXT 📜", callback_data="TXT"),
            ],
            [
                InlineKeyboardButton(text="🎄 CSV 🎄", callback_data="CSV"),
                InlineKeyboardButton(text="☃️ pickle ☃️ ", callback_data="pickle")
            ],
            # [InlineKeyboardButton(text="💼 Личный кабинет 💼 ", callback_data="kab")],
            [
                InlineKeyboardButton(
                    text="👨‍💻 Тех.поддержка 👨‍💻", callback_data="help"
                )
            ]
        ]
    )


def help_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Обратная связь", callback_data="feedback"),
                InlineKeyboardButton(text="Ответы на вопросы", callback_data="faq"),
            ],
            [InlineKeyboardButton(text="Будущие Функции", callback_data="WILL_FUNC")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
        ]
    )


def CSV_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Сохранить CSV", callback_data="CSV_add"
                ),
                InlineKeyboardButton(
                    text="Загрузить CSV", callback_data="CSV_load"
                )
            ],

            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
        ]
    )


def pickle_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Сохранить pickle", callback_data="pickle_add"
                ),
                InlineKeyboardButton(
                    text="Загрузить pickle", callback_data="pickle_load"
                )
            ],

            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
        ]
    )


def TXT_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Сохранить TXT", callback_data="TXT_add"
                ),
                InlineKeyboardButton(
                    text="Загрузить TXT", callback_data="TXT_load"
                )
            ],

            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
        ]
    )


def back_to_start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
        ]
    )


def back_to_help_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_help")]
        ]
    )


def back_to_CSV_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_CSV")]
        ]
    )


def back_to_pickle_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_pickle")]
        ]
    )

def back_to_TXT_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_TXT")]
        ]
    )