
import app.keyboards as kb
from aiogram import Router, F, Bot, types
from aiogram.types import Message, CallbackQuery, BufferedInputFile,Document,InputFile
import logging
import asyncio
import os
import re
import csv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import io
import pandas as pd
from aiogram.types.input_file import FSInputFile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

class UserState(StatesGroup):
    START = State()
    waiting_for_text = State()
    waiting_for_key_value = State()
    waiting_for_confirmation = State()
    waiting_for_key_value_more = State()
    waiting_for_file = State()
    waiting_menu = State() 

if not os.path.exists('Spam_TXT'):
    os.makedirs('Spam_TXT')

if not os.path.exists('Spam_CSV'):
    os.makedirs('Spam_CSV')

#####################################################################################################################################################

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
        "▪️ Выберите одну из опций ниже для получения дополнительной информации:\n\n"
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
        "- Здесь вы cможете сохранить текст в CSV файл, а также выбрать структуру файла или загрузить уже раннее сохраненный файл.\n\n"
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

#####################################################################################################################################################

@router.callback_query(lambda query: query.data == "Konvertart")
async def show_convert_file_message(query: CallbackQuery, state: FSMContext):
    convert_message = (
        "<b>Конвертация файлов</b>\n\n"
        "Уважаемые пользователи!\n\n"
        "Теперь вы можете конвертировать различные типы файлов в другие форматы прямо через нашего бота. Поддерживаемые форматы конвертации:\n\n"
        "1. TXT В CSV\n\n"
        ""
        "Пожалуйста, выберите цифру формата файлов которые хотите конвертировать.\n\n"
    )
    await state.set_state(UserState.waiting_menu)  # Устанавливаем состояние waiting_menu
    await query.message.edit_text(convert_message, parse_mode="HTML", reply_markup=kb.back_to_start_keyboard())
    await state.update_data(last_message_id=query.message.message_id)
    await query.answer()

@router.message(F.text.lower() == "1" or F.text.lower() == "один")
async def confirm_conversion(message: Message, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    if last_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    convert_message = ( "Пожалуйста, загрузите файл, который вы хотите конвертировать в csv.")
    sent_message = await message.answer(convert_message, parse_mode="HTML", reply_markup=kb.back_to_start_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(UserState.waiting_for_file)
    await asyncio.sleep(20)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)

@router.message(UserState.waiting_for_file, F.document)
async def process_file(message, state: FSMContext):
    document: Document = message.document
    file_id = document.file_id
    file_name = document.file_name

    # Проверка формата файла
    if not file_name.lower().endswith('.txt'):
        await message.answer("Пожалуйста, загрузите файл с расширением .txt.")
        return

    file = await message.bot.get_file(file_id)
    file_path = file.file_path

    # Скачиваем файл в память
    file_content = await message.bot.download_file(file_path)
    file_content = file_content.read().decode('utf-8')

    try:
        # Конвертация файла в CSV
        in_file = io.StringIO(file_content)
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        output_file = io.StringIO()
        writer = csv.writer(output_file)
        writer.writerows(lines)
        output_file.seek(0)

        # Отправка конвертированного файла
        document_to_send = BufferedInputFile(output_file.getvalue().encode('utf-8'), filename=f"{os.path.splitext(file_name)[0]}.csv")
        await message.answer_document(document=document_to_send)
    except UnicodeDecodeError as e:
        logger.error(f"UnicodeDecodeError: {e}")
        await message.answer("Ошибка при обработке файла. Пожалуйста, убедитесь, что файл содержит только поддерживаемые символы.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await message.answer("Произошла неожиданная ошибка. Пожалуйста, попробуйте еще раз.")

    await state.clear()
    await cmd_start(message, state) 

#####################################################################################################################################################

@router.callback_query(lambda query: query.data == "help")
async def Faq2(query: CallbackQuery, state: FSMContext):
    faq_txt = (
        "▫️ Выберите одну из опций ниже для получения дополнительной информации:\n\n"
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



#####################################################################################################################################################

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
        if message_id != query.message.message_id:  
            try:
                await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

    CSV_structure_message = "<b>Выберите структуру CSV файла: </b>\n\n"
    sent_message = await query.message.edit_text(
        CSV_structure_message,
        parse_mode="HTML",
        reply_markup=kb.CSV_structure(),
    )

    message_ids = [sent_message.message_id]
    await state.update_data(message_ids=message_ids)
    await query.answer()

@router.callback_query(lambda query: query.data == "key_value")
async def show_CSV_add_1str(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message_ids = user_data.get('message_ids', [])

    for message_id in message_ids:
        if message_id != query.message.message_id:  
            try:
                await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

    await state.set_state(UserState.waiting_for_key_value)
    await state.update_data(message_ids=[])
    sent_message = await query.message.edit_text(
        "Введите ваши элементы в формате 'ключ - значение':",
        reply_markup=kb.back_to_CSV_keyboard_STRUCTURE()
    )
    message_ids = [sent_message.message_id]
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
        error_message = await message.answer(f"Неверный формат. \n\nПожалуйста, введите только один элемент в формате 'ключ - значение'.")
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

    for message_id in message_ids:
        try:
            await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    await state.clear()
    await query.answer()

@router.message(UserState.waiting_for_key_value)
async def process_key_value(message: Message, state: FSMContext):
    user_data = await state.get_data()
    key_value_pairs = user_data.get('key_value_pairs', [])
    message_ids = user_data.get('message_ids', [])

    try:
        pattern = re.compile(r'(\w+)\s*-\s*(\w+)')
        matches = pattern.findall(message.text)

        for match in matches:
            key, value = match
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

@router.message(UserState.waiting_for_confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    user_data = await state.get_data()
    key_value_pairs = user_data.get('key_value_pairs', [])
    message_ids = user_data.get('message_ids', [])

    try:
        # Используем регулярное выражение для разбора строк
        pattern = re.compile(r'(\w+)\s*-\s*(\w+)')
        matches = pattern.findall(message.text)

        for match in matches:
            key, value = match
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

# Обработчик callback-запроса для отображения запроса на ввод данных в другом формате
@router.callback_query(lambda query: query.data == "key_value_more")
async def show_CSV_add_3str(query: CallbackQuery, state: FSMContext):
    CSV_add_3str_message = (
        "Введите ваши элементы в формате: \n\n"
        "1️⃣ - 'ключ - значение1, значение2'\n\n"
        "2️⃣ - 'ключ1, ключ2 - значение'"
    )
    sent_message = await query.message.edit_text(
        CSV_add_3str_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_CSV_keyboard(),
    )

    await state.set_state(UserState.waiting_for_key_value_more)
    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

# Обработчик сообщений для ввода данных в формате "ключ - значение1, значение2" и "ключ1, ключ2 - значение"
@router.message(UserState.waiting_for_key_value_more)
async def process_key_value_more(message: Message, state: FSMContext):
    user_data = await state.get_data()
    key_value_pairs = user_data.get('key_value_pairs', [])
    message_ids = user_data.get('message_ids', [])

    try:
        # Обработка формата "ключ - значение1, значение2"
        pattern1 = re.compile(r'(\w+)\s*-\s*([\w,]+)')
        matches1 = pattern1.findall(message.text)

        for match in matches1:
            key, values = match
            values_list = values.split(',')
            for value in values_list:
                key_value_pairs.append((key.strip(), value.strip()))

        # Обработка формата "ключ1, ключ2 - значение"
        pattern2 = re.compile(r'([\w,]+)\s*-\s*(\w+)')
        matches2 = pattern2.findall(message.text)

        for match in matches2:
            keys, value = match
            keys_list = keys.split(',')
            for key in keys_list:
                key_value_pairs.append((key.strip(), value.strip()))

        await state.update_data(key_value_pairs=key_value_pairs)
        await state.set_state(UserState.waiting_for_confirmation)
        sent_message = await message.answer("Хотите ввести еще одно значение?", reply_markup=kb.key_value_keyboard())
        message_ids.append(sent_message.message_id)
        message_ids.append(message.message_id)
        await state.update_data(message_ids=message_ids)
    except ValueError:
        error_message = await message.answer(f"Неверный формат. \n\nПожалуйста, введите в одном из форматов:\n\n1️⃣ - 'ключ - значение1, значение2'\n\n2️⃣ - 'ключ1, ключ2 - значение'.")
        message_ids.append(error_message.message_id)
        message_ids.append(message.message_id)
        await state.update_data(message_ids=message_ids)



@router.callback_query(lambda query: query.data == "CSV_load")
async def show_CSV_load(query: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Функция обработки кнопки "Загрузить CSV"
    """
    user_id = query.from_user.id
    file_name = f"Spam_CSV/CSV_{user_id}.csv"

    await query.message.delete()

    if os.path.exists(file_name):
        document = BufferedInputFile(open(file_name, 'rb').read(), filename=file_name)
        await bot.send_document(chat_id=query.message.chat.id, document=document, caption="Вот ваш CSV файл.")
    else:
        error_message = await bot.send_message(chat_id=query.message.chat.id, text="Файл не найден.")
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=error_message.message_id)
    CSV_message = (
        "<b>🧬 Работа с CSV файлами 🧬</b>\n\n"
        "- Здесь вы cможете сохранить текст в CSV файл, а также выбрать структуру файла или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )
    sent_message = await bot.send_message(
        chat_id=query.message.chat.id,
        text=CSV_message,
        parse_mode="HTML",
        reply_markup=kb.CSV_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()


#####################################################################################################################################################

@router.callback_query(lambda query: query.data == "pickle")
async def show_pickle(query: CallbackQuery, state: FSMContext):
    pickle_message = (
        "<b>⚖️ Работа с pickle файлами ⚖️</b>\n\n"
        "- Здесь вы можете сохранить текст в pickle файл или загрузить уже сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )
    sent_message = await query.message.edit_text(
        pickle_message, parse_mode="HTML", reply_markup=kb.pickle_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()


@router.callback_query(lambda query: query.data == "pickle_add")
async def show_pickle_add(query: CallbackQuery, state: FSMContext):
    pickle_add_message = (
    "<b>В данный момент функция pickle не доступна</b>\n\n"
    "Уважаемые пользователи!\n\n"
    "Мы временно приостановили работу функции сохранение pickle файлов для проведения технического обслуживания и улучшения сервиса. Мы стремимся предоставить вам лучший опыт использования, и для этого нам необходимо внести некоторые изменения.\n\n"
    "Пожалуйста, попробуйте воспользоваться этой функцией позже. Мы извиняемся за доставленные неудобства и благодарим вас за понимание.\n\n"
    "С уважением,\n"
    "Команда поддержки"
    )
    sent_message = await query.message.edit_text(
        pickle_add_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_pickle_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "pickle_load")
async def show_pickle_add(query: CallbackQuery, state: FSMContext):
    pickle_load_message = (
    "<b>В данный момент функция pickle не доступна</b>\n\n"
    "Уважаемые пользователи!\n\n"
    "Мы временно приостановили работу функции загрузки pickle файлов для проведения технического обслуживания и улучшения сервиса. Мы стремимся предоставить вам лучший опыт использования, и для этого нам необходимо внести некоторые изменения.\n\n"
    "Пожалуйста, попробуйте воспользоваться этой функцией позже. Мы извиняемся за доставленные неудобства и благодарим вас за понимание.\n\n"
    "С уважением,\n"
    "Команда поддержки"
    )
    sent_message = await query.message.edit_text(
        pickle_load_message,
        parse_mode="HTML",
        reply_markup=kb.back_to_pickle_keyboard(),
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

#####################################################################################################################################################

@router.callback_query(lambda query: query.data == "TXT")
async def show_TXT(query: CallbackQuery, state: FSMContext):
    TXT_message = (
        "<b>📝 Работа с TXT файлами 📝</b>\n\n"
        "- Здесь вы можете сохранить текст в TXT файл или загрузить уже сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )
    sent_message = await query.message.edit_text(
        TXT_message, parse_mode="HTML", reply_markup=kb.TXT_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

@router.callback_query(lambda query: query.data == "TXT_add")
async def show_TXT_add(query: CallbackQuery, state: FSMContext):
    TXT_add_message = "Отправьте текст, который хотите сохранить в TXT файл."

    prompt_message = await query.message.edit_text(
        TXT_add_message,
        reply_markup=kb.back_to_TXT_keyboard_MENU()
    )
    await state.set_state(UserState.waiting_for_text)
    await state.update_data(prompt_message_id=prompt_message.message_id)
    await query.answer()



@router.callback_query(lambda query: query.data == "TXT_load")
async def show_TXT_load(query: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = query.from_user.id
    file_name = f"Spam_TXT/TEXT_{user_id}.txt"

    await query.message.delete()

    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            await bot.send_document(chat_id=query.message.chat.id, document=BufferedInputFile(file.read(), filename=file_name), caption="Ваш TXT файл.")
    else:
        error_message = await bot.send_message(chat_id=query.message.chat.id, text="Файл не найден. Пожалуйста, сначала сохраните текст.")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=error_message.message_id)

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

#####################################################################################################################################################

@router.callback_query(lambda query: query.data == "WILL_FUNC")
async def show_WILL_FUNC(query: CallbackQuery, state: FSMContext):
    WILL_FUNC_massege = "<b>🐾 Наше будущее 🐾</b>\n\n В скором времени будут добавлены такие функции как:  \n\n - Конвертация файлов в другие форматы 🔄📝 \n - Преобразование текста в pickle файл ☃️ \n"
    sent_message = await query.message.edit_text(
        WILL_FUNC_massege, parse_mode="HTML", reply_markup=kb.back_to_start_keyboard()
    )

    await state.update_data(last_message_id=sent_message.message_id)
    await query.answer()

#####################################################################################################################################################

@router.callback_query(lambda query: query.data == "back_to_TXT_MENU")
async def back_to_TXT_MENU(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message_ids = user_data.get('message_ids', [])

    for message_id in message_ids:
        if message_id != query.message.message_id:
            try:
                await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

    back_to_TXT_MENU_message = (
        "<b>📝 Работа с TXT файлами 📝</b>\n\n"
        "Здесь вы можете сохранить текст в TXT файл или загрузить уже сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )

    sent_message = await query.message.edit_text(
        back_to_TXT_MENU_message,
        parse_mode="HTML",
        reply_markup=kb.TXT_keyboard(),  
    )

    message_ids = [sent_message.message_id]
    await state.update_data(message_ids=message_ids)
    await query.answer()
    

@router.callback_query(lambda query: query.data == "back_to_CSV_structure")
async def back_to_CSV_structure(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message_ids = user_data.get('message_ids', [])

    for message_id in message_ids:
        if message_id != query.message.message_id:
            try:
                await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

    CSV_structure_message = "<b>Выберите структуру CSV файла: </b>\n\n"
    sent_message = await query.message.edit_text(
        CSV_structure_message,
        parse_mode="HTML",
        reply_markup=kb.CSV_structure(),
    )

    message_ids = [sent_message.message_id]  
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

    for message_id in message_ids:
        if message_id != query.message.message_id:  
            try:
                await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

    CSV_message = (
        "<b>🧬 Работа с CSV файлами 🧬</b>\n\n"
        "- Здесь вы cможете сохранить текст в CSV файл, а также выбрать структуру файла или загрузить уже раннее сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"
    )
    sent_message = await query.message.edit_text(
        CSV_message, parse_mode="HTML", reply_markup=kb.CSV_keyboard()
    )

    message_ids = [sent_message.message_id]
    await state.update_data(message_ids=message_ids)
    await query.answer()


@router.callback_query(lambda query: query.data == "back_to_pickle")
async def back_to_pickle(query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    message_ids = user_data.get('message_ids', [])

    for message_id in message_ids:
        if message_id != query.message.message_id: 
            try:
                await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=message_id)
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

    pickle_message = (
        "<b>⚖️ Работа с pickle файлами ⚖️</b>\n\n"
        "- Здесь вы можете сохранить текст в pickle файл или загрузить уже сохраненный файл.\n\n"
        "Выберите одну из опций ниже ⬇️"        
    )
    sent_message = await query.message.edit_text(
        pickle_message, parse_mode="HTML", reply_markup=kb.pickle_keyboard()
    )

    message_ids = [sent_message.message_id]  #
    await state.update_data(message_ids=message_ids)
    await query.answer()

@router.callback_query(lambda query: query.data == "back_to_TXT")
async def back_to_TXT(query: CallbackQuery, state: FSMContext):
    try:
        await query.message.edit_text(
            (
                "<b>📝 Работа с TXT файлами 📝</b>\n\n"
                "- Здесь вы можете сохранить текст в TXT файл или загрузить уже сохраненный файл.\n\n"
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
