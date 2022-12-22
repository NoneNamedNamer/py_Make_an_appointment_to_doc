#Импорты
from aiogram import executor
from database_ import sqlite_users
from database_ import sqlite_db
from config.bot_config import dp
from handlers.admin_panel.aboutDoctors import *
from handlers.user_panel.aboutClients import *
from handlers.admin_panel.forDEL_rec import *
from handlers.test.test import *


async def on_startup(_):
    print("It's ok!")
    sqlite_db.sql_start()
    sqlite_users.sql_start()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)