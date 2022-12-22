from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from config.bot_config import dp, ADMIN, bot
from database_ import sqlite_users
from keyboards.admin_panel_keyboard_main_menu import button_case_admin
from keyboards.user_panel_keyboard_main_menu import kb_user
from database_ import sqlite_db

#Хендлер реагирует на комманду старт.
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if message.from_user.id == ADMIN:
        #Отправляем сообщение с клавиатурой
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Ваш ID: {message.from_user.id}.\n"
                                    f"Ваш статус: суперпользователь.",
                               reply_markup=button_case_admin)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Ваш ID: {message.from_user.id}.\n"
                                    f"Ваш статус: клиент.",
                               reply_markup=kb_user)

@dp.message_handler(commands=['Режим_работы'])
async def regime_check(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вт-Пт с 9:00 до 17:00')

@dp.message_handler(commands=['Расположение'])
async def place_check(message: types.Message):
    await bot.send_message(message.from_user.id, 'СПб, Проспект Большевиков, д. 23')

@dp.message_handler(commands=['Врачи'])
async def doctors_list(message: types.Message):
    await sqlite_db.sql_read(message)

class FSMclients(StatesGroup):
    name_cl = State()
    name_doc = State()
    date = State()
    time = State()

@dp.message_handler(commands=['Записаться'], state=None)
async def appoint_to(message: types.Message):
    await FSMclients.next()
    await message.reply('Введите свое ФИО')

@dp.message_handler(state=FSMclients.name_cl)
async def load_name_cl(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_cl'] = message.text
    await FSMclients.next()
    await message.reply('Введите данные предпочтительно врача')

@dp.message_handler(state=FSMclients.name_doc)
async def load_name_doc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_вщс'] = message.text
    await FSMclients.next()
    await message.reply('Введите предпочтительную дату')

@dp.message_handler(state=FSMclients.date)
async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await FSMclients.next()
    await message.reply('Введите предпочтительное время')

@dp.message_handler(state=FSMclients.time)
async def load_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await sqlite_users.sql_add_comm(state)
    await state.finish()

