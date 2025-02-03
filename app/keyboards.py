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
            [InlineKeyboardButton(text="✈️  Конвертация  ✈️", callback_data="Konvertart")],
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
                InlineKeyboardButton(text="Обратная связь 🧑🏻‍💻", callback_data="feedback"),
                InlineKeyboardButton(text="Ответы на вопросы 📑", callback_data="faq"),
            ],
            [InlineKeyboardButton(text="Будущие Функции 📈", callback_data="WILL_FUNC")],
            [InlineKeyboardButton(text="Назад 🔙", callback_data="back_to_start")],
        ]
    )


def CSV_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Сохранить CSV", callback_data="CSV_structure"
                ),
                InlineKeyboardButton(
                    text="Загрузить CSV", callback_data="CSV_load"
                )
            ],

            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
        ]
    )

def key_value_keyboard():
    return InlineKeyboardMarkup(
         inline_keyboard=[
            [InlineKeyboardButton(text="Прекратить", callback_data="stop_csv")]
        ]
    )

def pickle_key_value_keyboard():
    return InlineKeyboardMarkup(
         inline_keyboard=[
            [InlineKeyboardButton(text="Прекратить", callback_data="pickle_stop")]
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


def CSV_structure():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ключ: значение",
                    callback_data="key_value" 
                )
            ],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_CSV")]
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

def back_to_CSV_keyboard_STRUCTURE():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_CSV_structure")]
        ]
    )

def back_to_TXT_keyboard_MENU():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_TXT_MENU")]
        ]
    )
