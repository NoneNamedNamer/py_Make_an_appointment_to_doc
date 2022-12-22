from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from config.bot_config import dp, bot, ADMIN
from database_ import sqlite_db
from keyboards.admin_panel_keyboard_main_menu import button_case_admin


class FSMdoctors(StatesGroup):
    photo = State()
    name = State()
    experience = State()
    price = State()

@dp.message_handler(commands=['moderator'])
async def make_changes_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вносим изменения',
    reply_markup=button_case_admin)
    await message.delete()

@dp.message_handler(state="*", commands='отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

#Начало диалога загрузки нового пункта меню
@dp.message_handler(commands=['Добавить'], state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ADMIN:
        await FSMdoctors.photo.set()
        await message.reply('Загружаем фото врача')

@dp.message_handler(content_types=['photo'], state=FSMdoctors.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMdoctors.next()
    await message.reply("Теперь вводим ФИО врача")

@dp.message_handler(state=FSMdoctors.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMdoctors.next()
    await message.reply('Теперь вводим его опыт работы')

@dp.message_handler(state=FSMdoctors.experience)
async def load_experience(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience'] = message.text
    await FSMdoctors.next()
    await message.reply('Теперь указываем цену за приём')

@dp.message_handler(state=FSMdoctors.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await sqlite_db.sql_add_command(state)
    await state.finish()

