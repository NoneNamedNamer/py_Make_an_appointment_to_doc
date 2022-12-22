import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('stomatologic_clin.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS clients(name_cl TEXT PRIMARY KEY, name_doc TEXT, date TEXT, time TEXT)')
    base.commit()

async def sql_add_comm(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO clients VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()