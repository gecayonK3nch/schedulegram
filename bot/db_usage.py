import sqlite3
import os
from get_stations import stations
from datetime import datetime

def get_schedule(_from: str, _to: str, _date: str, show_gone: bool) -> str:
    date = datetime.strptime(_date, "%Y-%m-%d").date()
    con = sqlite3.connect("././database/schedule.db")
    cur = con.cursor()
    sql_req = "SELECT arrival_time, departure_time, type, price FROM schedule WHERE date = ? AND departure_station = ? AND arrival_station = ?"

    if not cur.execute(sql_req, (_date, _from, _to)).fetchall():
        os.system(os.path.abspath(os.curdir) + f"/parser/build/Debug/parser.exe {_from} {_to} {_date}")

    if show_gone:
        res = cur.execute(sql_req, (_date, _from, _to)).fetchall()
    else:
        sql_req = "SELECT arrival_time, departure_time, type, price FROM schedule WHERE date = ? AND departure_station = ? AND arrival_station = ? AND price != ?"
        res = cur.execute(sql_req, (_date, _from, _to, "Ушел")).fetchall()

    if _date == datetime.now().date().strftime("%Y-%m-%d"):
        to_del: list[tuple[str]] = []
        for row in res:
            if datetime.strptime(row[1], "%H:%M").time() < datetime.now().time():
                if show_gone:
                    res[res.index(row)] = tuple(row[i] if i != 3 else "Ушел" for i in range(len(row)))
                else:
                    to_del.append(row)
        for row in to_del:
            res.remove(row)

    answer = f"Расписание поездов {stations[_from]}-{stations[_to]} на {"{:%d.%m.%Y}".format(date)}\n\nОтправление | Прибытие |    Тип  поезда    | Цена\n------------|----------|-------------------|-----\n"

    answer += '\n'.join([f"◦{row[1]:^11}|{row[0]:^10}|{row[2]:^19}|{row[3]:^6}\n" for row in res])

    return answer
