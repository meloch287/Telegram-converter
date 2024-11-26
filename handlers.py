import app.keyboards as kb
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram import types
import logging
import asyncio
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

class UserState(StatesGroup):
    START = State()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    """
    Функция команды старт, вызывает окно по команде /start
    """
    user_nickname = (
        message.from_user.username
        if message.from_user.username
        else "Уважаемый пользователь"
    )

    welcome_message = (
        "<b>🌸 Добро пожаловать в Daydream! 🌸</b>\n\n"
        "- Здесь вы сможете преобразовать текстовые строки в различные файлы, такие как TXT, Pickle и CSV.\n\n"
        "Выберите одну из опций ниже, чтобы начать:"
    )

    await state.set_state(UserState.START)
    sent_message = await message.answer(
        welcome_message,
        parse_mode="HTML",
        reply_markup=kb.start_keyboard(),
    )
    await state.update_data(last_message_id=sent_message.message_id)


@router.message(F.text == "/help")
async def Faq1(message: Message, state: FSMContext):
    """
    Функция комманды /help
    """
    faq_txt = (
        "Выберите одну из опций ниже для получения дополнительной информации:\n\n"
        "- <b>Ответы на вопросы:</b> Узнайте больше о функциональности бота и как им пользоваться.\n\n"
        "- <b>Обратная связь:</b> Свяжитесь с нашей службой поддержки для получения помощи."
    )

    sent_message = await message.answer(
        faq_txt, parse_mode="HTML", reply_markup=kb.help_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

@router.message(F.text == "/CSV")
async def CSV(message: Message, state: FSMContext):
    """
    Функция команды /CSV, подсчитывает расходы
    """
    CSV_message = "<b>...</b>\n\n" ""

    sent_message = await message.answer(
        CSV_message, parse_mode="HTML", reply_markup=kb.CSV_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

@router.message(F.text == "/pickle")
async def pickle(message: Message, state: FSMContext):
    """
    Функция команды /pickle, подсчитывает расходы
    """
    pickle_message = "<b>...</b>\n\n" ""

    sent_message = await message.answer(
        pickle_message, parse_mode="HTML", reply_markup=kb.pickle_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

@router.message(F.text == "/TXT")
async def TXT(message: Message, state: FSMContext):
    """
    Функция команды /TXT, подсчитывает расходы
    """
    TXT_message = "<b>...</b>\n\n" ""

    sent_message = await message.answer(
        TXT_message, parse_mode="HTML", reply_markup=kb.TXT_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

# Обработчики
@router.callback_query(lambda query: query.data == "help")
async def Faq2(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Тех. поддержка"
    """
    faq_txt = (
        "Выберите одну из опций ниже для получения дополнительной информации:\n\n"
        "- <b>Ответы на вопросы:</b> Узнайте больше о функциональности бота и как им пользоваться.\n\n"
        "- <b>Обратная связь:</b> Свяжитесь с нашей службой поддержки для получения помощи."
    )

    sent_message = await query.message.edit_text(
        faq_txt, parse_mode="HTML", reply_markup=kb.help_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "faq")
async def show_faq(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "ответы на вопросы"
    """
    faq_details = (
        "<b>Ответы на вопросы:</b>\n\n"
    )

    sent_message = await query.message.edit_text(
        faq_details, parse_mode="HTML", reply_markup=kb.back_to_help_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "feedback")
async def show_feedback(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Обратная связь"
    """
    feedback_details = (
        "<b>Обратная связь:</b>\n\n"
        "Если у вас возникли вопросы или проблемы, свяжитесь с нашей службой поддержки  --> (@jokessssv)"
    )
    sent_message = await query.message.edit_text(
        feedback_details, parse_mode="HTML", reply_markup=kb.back_to_help_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "CSV")
async def show_CSV(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "CSV"
    """
    CSV_message = "<b>...</b>\n\n" ""
    sent_message = await query.message.edit_text(
        CSV_message, parse_mode="HTML", reply_markup=kb.CSV_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "CSV_add")
async def show_CSV_add(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Сохранить CSV"
    """
    CSV_add_message = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        CSV_add_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_CSV_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "CSV_load")
async def show_CSV_add(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Загрузить CSV"
    """
    CSV_load_message = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        CSV_load_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_CSV_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "pickle")
async def show_pickle(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "pickle"
    """
    pickle_message = "<b>...</b>\n\n" ""
    sent_message = await query.message.edit_text(
        pickle_message, parse_mode="HTML", reply_markup=kb.pickle_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "pickle_add")
async def show_pickle_add(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Сохранить pickle"
    """
    pickle_add_message = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        pickle_add_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_pickle_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "pickle_load")
async def show_pickle_add(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Загрузить pickle"
    """
    pickle_load_message = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        pickle_load_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_pickle_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "TXT")
async def show_TXT(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "TXT"
    """
    TXT_message = "<b>...</b>\n\n" ""
    sent_message = await query.message.edit_text(
        TXT_message, parse_mode="HTML", reply_markup=kb.TXT_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "TXT_add")
async def show_pickle_add(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Сохранить TXT"
    """
    TXT_add_message = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        TXT_add_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_TXT_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "TXT_load")
async def show_pickle_add(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Загрузить TXT"
    """
    TXT_load_message = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        TXT_load_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_TXT_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "WILL_FUNC")
async def show_WILL_FUNC(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Будущие функции"
    """
    WILL_FUNC_massege = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        WILL_FUNC_massege, parse_mode="HTML", reply_markup=kb.back_to_help_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "back_to_start")
async def back_to_start(query: CallbackQuery, state: FSMContext):
    """Обработчик возвращения к стартовому меню"""
    try:
        await query.message.edit_text(
            "<b>🌸 Добро пожаловать в Daydream! 🌸</b>\n\n"
            "- Здесь вы сможете преобразовать текстовые строки в различные файлы, такие как TXT, Pickle и CSV.\n\n"
            "Выберите одну из опций ниже, чтобы начать:",
            parse_mode="HTML",
            reply_markup=kb.start_keyboard(),
        )
    except Exception as e:
        print(f"Ошибка: {e}")

    await state.set_state(UserState.START)

@router.callback_query(lambda query: query.data == "back_to_help")
async def back_to_help(query: CallbackQuery, state: FSMContext):
    """Обработчик кнопки "назад" к окну с коммандой /help"""
    try:
        await query.message.edit_text(
            "Выберите одну из опций ниже для получения дополнительной информации:\n\n"
            "- <b>Ответы на вопросы:</b> Узнайте больше о функциональности бота и как им пользоваться.\n\n"
            "- <b>Обратная связь:</b> Свяжитесь с нашей службой поддержки для получения помощи.",
            parse_mode="HTML",
            reply_markup=kb.help_keyboard(),
        )
    except Exception as e:
        print(f"Error occurred while going back: {e}")

@router.callback_query(lambda query: query.data == "back_to_CSV")
async def back_to_CSV(query: CallbackQuery, state: FSMContext):
    """Обработчик кнопки "назад" к окну с коммандой /CSV (CSV)"""
    try:
        await query.message.edit_text(
            "<b>...</b>\n\n",
            parse_mode="HTML",
            reply_markup=kb.CSV_keyboard(),
        )
    except Exception as e:
        print(f"Error occurred while going back: {e}")

@router.callback_query(lambda query: query.data == "back_to_pickle")
async def back_to_pickle(query: CallbackQuery, state: FSMContext):
    """Обработчик кнопки "назад" к окну с коммандой /pickle (pickle)"""
    try:
        await query.message.edit_text(
            "<b>...</b>\n\n",
            parse_mode="HTML",
            reply_markup=kb.pickle_keyboard(),
        )
    except Exception as e:
        print(f"Error occurred while going back: {e}")

@router.callback_query(lambda query: query.data == "back_to_TXT")
async def back_to_TXT(query: CallbackQuery, state: FSMContext):
    """Обработчик кнопки "назад" к окну с коммандой /TXT (TXT)"""
    try:
        await query.message.edit_text(
            "<b>...</b>\n\n",
            parse_mode="HTML",
            reply_markup=kb.TXT_keyboard(),
        )
    except Exception as e:
        print(f"Error occurred while going back: {e}")
