
import app.keyboards as kb
from aiogram import Router, F, Bot, types
from aiogram.types import Message, CallbackQuery, BufferedInputFile
import logging
import asyncio
import os
import re
import csv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

class UserState(StatesGroup):
    START = State()
    waiting_for_text = State()
    waiting_for_key_value = State()
    waiting_for_confirmation = State()

if not os.path.exists('Spam_TXT'):
    os.makedirs('Spam_TXT')

if not os.path.exists('Spam_CSV'):
    os.makedirs('Spam_CSV')

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
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
    CSV_message = (
        "<b>🧬 Работа с CSV файлами 🧬</b>\n\n"
        "Здесь вы cможете сохранить текст в CSV файл, а также выбрать структуру файла или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )

    sent_message = await message.answer(
        CSV_message, parse_mode="HTML", reply_markup=kb.CSV_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

@router.message(F.text == "/pickle")
async def pickle(message: Message, state: FSMContext):
    pickle_message = (
        "<b>⚖️ Работа с pickle файлами ⚖️</b>\n\n"
        "Здесь вы cможете сохранить текст в pickle файл или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )

    sent_message = await message.answer(
        pickle_message, parse_mode="HTML", reply_markup=kb.pickle_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

@router.message(F.text == "/TXT")
async def TXT(message: Message, state: FSMContext):
    TXT_message = (
        "<b>📝 Работа с TXT файлами 📝</b>\n\n"
        "Здесь вы можете сохранить текст в TXT файл или загрузить уже сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )

    sent_message = await message.answer(
        TXT_message, parse_mode="HTML", reply_markup=kb.TXT_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)

@router.callback_query(lambda query: query.data == "help")
async def Faq2(query: CallbackQuery, state: FSMContext):
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

@router.callback_query(lambda query: query.data == "CSV_structure")
async def show_CSV_structure(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message_ids = user_data.get('message_ids', [])

    for message_id in message_ids:
        try:
            await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    try:
        await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")

    CSV_structure_message = "<b>Выберите структуру CSV файла: </b>\n\n"
    sent_message = await query.message.answer(
        CSV_structure_message,
        parse_mode="HTML",
        reply_markup=kb.CSV_structure(),
    )

    message_ids = [sent_message.message_id]  # Обновляем список message_ids
    await state.update_data(message_ids=message_ids)
    await query.answer()

@router.callback_query(lambda query: query.data == "key_value")
async def show_CSV_add_1str(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message_ids = user_data.get('message_ids', [])

    # Удаление предыдущих сообщений
    for message_id in message_ids:
        try:
            await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    await state.set_state(UserState.waiting_for_key_value)
    await state.update_data(message_ids=[])
    sent_message = await query.message.answer("Введите ключ и значение в формате 'ключ - значение':", reply_markup=kb.back_to_CSV_keyboard_STRUCTURE())
    message_ids = [sent_message.message_id]  # Обновляем список message_ids
    await state.update_data(message_ids=message_ids)
    await query.answer()

@router.message(UserState.waiting_for_key_value)
async def process_key_value(message: Message, state: FSMContext):
    user_data = await state.get_data()
    key_value_pairs = user_data.get('key_value_pairs', [])
    message_ids = user_data.get('message_ids', [])

    try:
        key, value = message.text.split(' - ')
        key_value_pairs.append((key, value))
        await state.update_data(key_value_pairs=key_value_pairs)
        await state.set_state(UserState.waiting_for_confirmation)
        sent_message = await message.answer("Хотите ввести еще одно значение?", reply_markup=kb.key_value_keyboard())
        message_ids.append(sent_message.message_id)
        message_ids.append(message.message_id)
        await state.update_data(message_ids=message_ids)
    except ValueError:
        error_message = await message.answer(f"Неверный формат. \n\nПожалуйста, введите в формате 'ключ - значение'.")
        message_ids.append(error_message.message_id)
        message_ids.append(message.message_id)
        await state.update_data(message_ids=message_ids)

@router.callback_query(lambda query: query.data == "stop_csv")
async def stop_csv(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    key_value_pairs = user_data.get('key_value_pairs', [])
    message_ids = user_data.get('message_ids', [])

    if key_value_pairs:
        user_id = query.from_user.id
        file_name = f"Spam_CSV/CSV_{user_id}.csv"

        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ключ : значение"])
            for key, value in key_value_pairs:
                writer.writerow([f"{key} : {value}"])

        await query.message.answer(f"CSV файл успешно сохранен как {file_name}", reply_markup=kb.back_to_CSV_keyboard())
    else:
        await query.message.answer("Нет данных для сохранения.", reply_markup=kb.back_to_CSV_keyboard())

    # Удаление всех предыдущих сообщений
    for message_id in message_ids:
        try:
            await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    await state.clear()
    await query.answer()

@router.message(UserState.waiting_for_confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    user_data = await state.get_data()
    key_value_pairs = user_data.get('key_value_pairs', [])
    message_ids = user_data.get('message_ids', [])

    try:
        key, value = message.text.split(' - ')
        key_value_pairs.append((key, value))
        await state.update_data(key_value_pairs=key_value_pairs)
        sent_message = await message.answer("Хотите ввести еще одно значение?", reply_markup=kb.key_value_keyboard())
        message_ids.append(sent_message.message_id)
        message_ids.append(message.message_id)
        await state.update_data(message_ids=message_ids)
    except ValueError:
        error_message = await message.answer("Неверный формат. Пожалуйста, введите в формате 'ключ - значение'.")
        message_ids.append(error_message.message_id)
        message_ids.append(message.message_id)
        await state.update_data(message_ids=message_ids)

@router.callback_query(lambda query: query.data == "key_value_more")
async def show_CSV_add_3str(query: CallbackQuery, state: FSMContext):
    CSV_add_3str_message = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        CSV_add_3str_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_CSV_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "CSV_load")
async def show_CSV_load(query: CallbackQuery, state: FSMContext):
    """
    Функция обработки кнопки "Загрузить CSV"
    """
    user_id = query.from_user.id
    file_name = f"Spam_csv/CSV_{user_id}.csv"

    if os.path.exists(file_name):
        document = BufferedInputFile(open(file_name, 'rb').read(), filename=file_name)
        await query.message.answer_document(document, caption="Вот ваш CSV файл.")
    else:
        await query.message.answer("Файл не найден.")

    await query.answer()

@router.callback_query(lambda query: query.data == "pickle_add")
async def show_pickle_add(query: CallbackQuery, state: FSMContext):
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

@router.callback_query(lambda query: query.data == "TXT_add")
async def show_TXT_add(query: CallbackQuery, state: FSMContext):
    prompt_message = await query.message.answer("Отправьте текст, который хотите сохранить в TXT файл.")
    await state.set_state(UserState.waiting_for_text)
    await state.update_data(prompt_message_id=prompt_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "TXT_load")
async def show_TXT_load(query: CallbackQuery, state: FSMContext, bot: Bot):
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
    WILL_FUNC_massege = "<b>Временно недоступно 😢</b>\n\n"
    sent_message = await query.message.edit_text(
        WILL_FUNC_massege, parse_mode="HTML", reply_markup=kb.back_to_help_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "back_to_CSV_structure")
async def back_to_CSV_structure(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message_ids = user_data.get('message_ids', [])

    # Удаление предыдущих сообщений
    for message_id in message_ids:
        try:
            await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    # Удаление сообщения "🧬 Работа с SCV файлами 🧬"
    try:
        await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")

    CSV_structure_message = "<b>Выберите структуру CSV файла: </b>\n\n"
    sent_message = await query.message.answer(
        CSV_structure_message,
        parse_mode="HTML",
        reply_markup=kb.CSV_structure(),
    )

    message_ids.append(sent_message.message_id)
    await state.update_data(message_ids=message_ids)
    await query.answer()

@router.callback_query(lambda query: query.data == "back_to_start")
async def back_to_start(query: CallbackQuery, state: FSMContext):
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
    user_data = await state.get_data()
    message_ids = user_data.get('message_ids', [])

    # Удаление предыдущих сообщений
    for message_id in message_ids:
        try:
            await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    # Удаление текущего сообщения
    try:
        await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")

    CSV_message = (
        "<b>🧬 Работа с CSV файлами 🧬</b>\n\n"
        "Здесь вы cможете сохранить текст в CSV файл, а также выбрать структуру файла или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )
    sent_message = await query.message.answer(
        CSV_message, parse_mode="HTML", reply_markup=kb.CSV_keyboard()
    )

    message_ids = [sent_message.message_id]  # Обновляем список message_ids
    await state.update_data(message_ids=message_ids)
    await query.answer()

@router.callback_query(lambda query: query.data == "back_to_TXT")
async def back_to_TXT(query: CallbackQuery, state: FSMContext):
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

@router.message(F.text.startswith("/"))
async def handle_command(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    current_state = await state.get_state()
    if current_state != UserState.waiting_for_text:
        last_message_id = data.get('last_message_id')
        if last_message_id:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

    await cmd_start(message, state)

@router.message()
async def handle_unknown_message(message: Message, bot: Bot):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")

    unknown_message = await message.answer("Неизвестная команда. Пожалуйста, используйте одну из доступных команд.")
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=message.chat.id, message_id=unknown_message.message_id)

