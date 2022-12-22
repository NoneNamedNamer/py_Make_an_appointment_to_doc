from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.bot_config import dp, bot, ADMIN
from aiogram import types
from database_ import sqlite_db

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")}, удален.', show_alert=True)

@dp.message_handler(commands=['Удалить'])
async def delete_rec(message: types.Message):
    read = await sqlite_db.sql_read2()
    if message.from_user.id == ADMIN:
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0],
                                f'{ret[1]}\nОпыт работы: {ret[2]}\n'
                                f'Цена за прием: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))