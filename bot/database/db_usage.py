import sqlite3
import os
from database.get_stations import stations
from datetime import datetime, timedelta, timezone

# Парсит строку смещения временной зоны в объект timezone
def parse_offset(tz_str: str):
    sign = 1 if tz_str[0] != '-' else -1
    h, m = map(int, tz_str[1:].split(':'))
    return timezone(sign * timedelta(hours=h, minutes=m))

# Получает расписание поездов между двумя станциями на определенную дату
def get_schedule(_from: str, _to: str, _date: str, show_gone: bool) -> str:
    date = datetime.strptime(_date, "%Y-%m-%d").date()
    con = sqlite3.connect("././database/schedule.db")
    cur = con.cursor()

    # Внутренняя функция для выборки данных из базы
    def fetch(with_parser: bool = False, check_gone: bool = True):
        if with_parser:
            print("No data found, running parser...")
            os.system(os.path.abspath(os.curdir)
                      + f"/parser/build/Release/parser.exe {_from} {_to} {_date}")

        if check_gone:
            sql = (
                "SELECT arrival_time, departure_time, type, price, timezone "
                "FROM schedule "
                "WHERE date=? AND departure_station=? AND arrival_station=?"
            )
            params = (_date, _from, _to)
        else:
            sql = (
                "SELECT arrival_time, departure_time, type, price, timezone "
                "FROM schedule "
                "WHERE date=? AND departure_station=? AND arrival_station=? "
                "AND price != ?"
            )
            params = (_date, _from, _to, "Ушел")

        return cur.execute(sql, params).fetchall()
    
    try:
        res = fetch()
    except sqlite3.OperationalError:
        print("Database not found, creating a new one...")
        res = fetch(with_parser=True, check_gone=show_gone)
    if not res:
        res = fetch(with_parser=True, check_gone=show_gone)

    # Если дата сегодня, помечаем ушедшие поезда или удаляем их из результата
    if _date == datetime.now().date().strftime("%Y-%m-%d"):
        to_del: list[tuple[str]] = []
        for row in res:
            timezone = parse_offset(row[-1])
            if datetime.strptime(row[1], "%H:%M").time() < datetime.now(timezone).time():
                if show_gone:
                    res[res.index(row)] = tuple(row[i] if i != 3 else "Ушел" for i in range(len(row)))
                else:
                    to_del.append(row)
        for row in to_del:
            res.remove(row)

    # Формируем заголовок и тело расписания
    header = (
        f"Расписание поездов {stations[_from]}–{stations[_to]} "
        f"на {"{:%d.%m.%Y}".format(date)}\n\n"
        "Отправление | Прибытие |    Тип  поезда    | Цена\n"
        "------------|----------|-------------------|-----\n"
    )

    body = '\n'.join([f"◦{row[1]:^11}|{row[0]:^10}|{row[2]:^19}|{row[3]:^6}\n" for row in res])

    con.close()
    return header + body if res else "Все поезда ушли или не найдены."

# Асинхронная функция очистки базы от устаревших записей
async def clearing_db():
    con = sqlite3.connect("./database/schedule.db")
    cur = con.cursor()
    sql_req = "DELETE FROM schedule WHERE date < ?"
    now = datetime.now().strftime(format="%Y-%m-%d")
    res = cur.execute(sql_req, (now,))
    con.commit()
    con.close()
    print(f"table cleaned with exit code {res}", now)

# Асинхронная функция создания таблицы пользователей
async def create_users_table():
    con = sqlite3.connect("./database/schedule.db")
    cur = con.cursor()
    sql_req = ("CREATE TABLE IF NOT EXISTS users(" 
                "id INTEGER NOT NULL PRIMARY KEY, "
                "is_banned BOOL NOT NULL);"
                )
    cur.execute(sql_req)
    con.commit()
    con.close()
    print("Users table created succesfully")

# Асинхронная функция добавления пользователя или снятия бана
async def add_user(user_id: int):
    con = sqlite3.connect("./database/schedule.db")
    cur = con.cursor()
    try:
        sql_req = ("INSERT INTO users (id, is_banned) VALUES (?, ?);")
        cur.execute(sql_req, (user_id, False))
    except sqlite3.IntegrityError:
        sql_req = ("UPDATE users SET is_banned = ? WHERE id = ?;")
        cur.execute(sql_req, (False, user_id))
    con.commit()
    con.close()

# Асинхронная функция бана пользователя
async def user_banned(user_id: int):
    con = sqlite3.connect("./database/schedule.db")
    cur = con.cursor()
    sql_req = ("UPDATE users SET is_banned = ? WHERE id = ?;")
    cur.execute(sql_req, (True, user_id))
    con.commit()
    con.close()

# Асинхронная функция получения всех не забаненных пользователей
async def get_users():
    con = sqlite3.connect("./database/schedule.db")
    cur = con.cursor()
    sql_req = "SELECT id FROM users WHERE is_banned = ?;"
    res = cur.execute(sql_req, (False,)).fetchall()
    con.close()
    return [row[0] for row in res]

# Тестовая функция для запуска из консоли
def main() -> int:
    _from = str(input("Введите код отправления: "))
    _to = str(input("Введите код прибытия: "))
    _date = str(input("Введите дату в формате ГГГГ-ММ-ДД: "))
    try:
        print(get_schedule(_from, _to, _date, True))
        return 0
    except:
        return 1

if __name__ == "__main__":
    if main():
        print("Process ended with exit code 1")
