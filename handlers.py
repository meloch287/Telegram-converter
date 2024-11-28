import app.keyboards as kb
from aiogram import Router, F, Bot, types
from aiogram.types import Message, CallbackQuery,BufferedInputFile
import logging
import asyncio
import os
import re
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

class UserState(StatesGroup):
    START = State()
    waiting_for_text = State()
    

if not os.path.exists('Spam_TXT'):
    os.makedirs('Spam_TXT')

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
    Функция команды /CSV
    """
    CSV_message = (
        "<b>🧬 Работа с SCV файлами 🧬</b>\n\n"
        "Здесь вы cможете сохранить текст в SCV файл, а также выбрать структуру файла или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )

    sent_message = await message.answer(
        CSV_message, parse_mode="HTML", reply_markup=kb.CSV_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

@router.message(F.text == "/pickle")
async def pickle(message: Message, state: FSMContext):
    """
    Функция команды /pickle
    """
    pickle_message = ( "<b>⚖️ Работа с pickle файлами ⚖️</b>\n\n"
        "Здесь вы cможете сохранить текст в pickle файл или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )


    sent_message = await message.answer(
        pickle_message, parse_mode="HTML", reply_markup=kb.pickle_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

@router.message(F.text == "/TXT")
async def TXT(message: Message, state: FSMContext):
    """
    Функция команды /TXT
    """
    TXT_message = (
    "<b>📝 Работа с TXT файлами 📝</b>\n\n"
    "Здесь вы можете сохранить текст в TXT файл или загрузить уже сохраненный файл.\n\n"
    "Выберите одну из опций ниже ⬇️"
    )

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
    CSV_message = (
        "<b>🧬 Работа с SCV файлами 🧬</b>\n\n"
        "Здесь вы cможете сохранить текст в SCV файл, а также выбрать структуру файла или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )
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
    pickle_message =( 
        "<b>⚖️ Работа с pickle файлами ⚖️</b>\n\n"
        "Здесь вы cможете сохранить текст в pickle файл или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️")
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
    TXT_message = (
        "<b>📝 Работа с TXT файлами 📝</b>\n\n"
        "Здесь вы можете сохранить текст в TXT файл или загрузить уже сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )
    sent_message = await query.message.edit_text(
        TXT_message, parse_mode="HTML", reply_markup=kb.TXT_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

# Обработчик для кнопки "Сохранить TXT"
@router.callback_query(lambda query: query.data == "TXT_add")
async def show_TXT_add(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Сохранить TXT"
    """
    prompt_message = await query.message.answer("Отправьте текст, который хотите сохранить в TXT файл.")
    await state.set_state(UserState.waiting_for_text)
    await state.update_data(prompt_message_id=prompt_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "TXT_load")
async def show_TXT_load(query: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Функция обработки кнопки "Загрузить TXT"
    """
    user_id = query.from_user.id
    file_name = f"Spam_TXT/TEXT_{user_id}.txt"

    # Удаляем менюшку
    await query.message.delete()

    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            await bot.send_document(chat_id=query.message.chat.id, document=BufferedInputFile(file.read(), filename=file_name), caption="Ваш TXT файл.")
    else:
        error_message = await bot.send_message(chat_id=query.message.chat.id, text="Файл не найден. Пожалуйста, сначала сохраните текст.")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=error_message.message_id)

    # Удаляем предыдущее сообщение
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    if last_message_id:
        try:
            await bot.delete_message(chat_id=query.message.chat.id, message_id=last_message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    await TXT(query.message, state)

# Обработчик текста
@router.message(UserState.waiting_for_text)
async def process_text(message: types.Message, state: FSMContext, bot: Bot):
    # Проверка наличия текста в сообщении
    if message.text is None:
        error_message = await message.answer("Неверный формат. Попробуйте снова.")
        await asyncio.sleep(1)
        await bot.delete_message(chat_id=message.chat.id, message_id=error_message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return

    user_id = message.from_user.id
    file_name = f"Spam_TXT/TEXT_{user_id}.txt"

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(message.text)

    success_message = await message.answer("Успешно сохранено")
    await asyncio.sleep(1)
    await success_message.delete()

    # Удаляем все предыдущие сообщения
    data = await state.get_data()
    prompt_message_id = data.get('prompt_message_id')
    last_message_id = data.get('last_message_id')
    logger.info(f"prompt_message_id: {prompt_message_id}, last_message_id: {last_message_id}")
    if prompt_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=prompt_message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")
    if last_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    await asyncio.sleep(0.5)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await TXT(message, state)


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

        "<b>🧬 Работа с SCV файлами 🧬</b>\n\n"
        "Здесь вы cможете сохранить текст в SCV файл, а также выбрать структуру файла или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️",
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
                "<b>⚖️ Работа с pickle файлами ⚖️</b>\n\n"
                "Здесь вы cможете сохранить текст в pickle файл или загрузить уже раннее сохраненный файл.\n\n"
                "Выберите одну из опций ниже ⬇️",
            parse_mode="HTML",
            reply_markup=kb.pickle_keyboard(),
        )
    except Exception as e:
        print(f"Error occurred while going back: {e}")

@router.callback_query(lambda query: query.data == "back_to_TXT")
async def back_to_TXT(query: CallbackQuery, state: FSMContext):
    """Обработчик кнопки "назад" к окну с командой /TXT (TXT)"""
    try:
        await query.message.edit_text(
            (
                "<b>📝 Работа с TXT файлами 📝</b>\n\n"
                "Здесь вы можете сохранить текст в TXT файл или загрузить уже сохраненный файл.\n\n"
                "Выберите одну из опций ниже ⬇️"
            ),
            parse_mode="HTML",
            reply_markup=kb.TXT_keyboard(),
        )
    except Exception as e:
        print(f"Error occurred while going back: {e}")



# Обработчик для команд
@router.message(F.text.startswith("/"))
async def handle_command(message: Message, state: FSMContext, bot: Bot):
    """
    Обработчик для команд
    """
    # Удаляем все предыдущие сообщения, если пользователь не находится в состоянии ожидания текста
    data = await state.get_data()
    current_state = await state.get_state()
    if current_state != UserState.waiting_for_text:
        last_message_id = data.get('last_message_id')
        if last_message_id:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

    # Обрабатываем команду
    await cmd_start(message, state)

# Обработчик для неизвестных сообщений
@router.message()
async def handle_unknown_message(message: Message, bot: Bot):
    """
    Обработчик для неизвестных сообщений
    """
    # Удаляем неизвестное сообщение
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")

    # Уведомляем пользователя о неизвестной команде
    unknown_message = await message.answer("Неизвестная команда. Пожалуйста, используйте одну из доступных команд.")
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=message.chat.id, message_id=unknown_message.message_id)
