import datetime
import sqlite3
from sql_scripts import *


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('FIRM.db')
        self.c = self.conn.cursor()
        self.c.executescript(INIT_DB)
        self.conn.commit()

    def register_user(self, code, fio, type_user, number, mail):
        data = datetime.datetime.now().strftime('%d.%m.%Y')
        time = datetime.datetime.now().strftime('%H:%M:%S')
        self.c.execute(INSERT_USER, (code, fio, type_user, number, mail))
        self.c.execute(INSERT_VISIT, (code, data, time, 0))
        self.conn.commit()

    def scan_employee(self, employee_id):
        data = datetime.datetime.now().strftime('%d.%m.%Y')
        time = datetime.datetime.now().strftime('%H:%M:%S')
        self.c.execute(GET_STATUS, (employee_id, data))
        status = self.c.fetchone()
        status = status[0] if status else 0

        self.c.execute(INSERT_VISIT, (employee_id, data, time, not status))

        self.conn.commit()

    def find_users(self, user_type):
        self.c.execute(USER_TYPE, (user_type,))
        self.conn.commit()
        lst = self.c.fetchall()

        return lst

