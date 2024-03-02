import datetime
import sqlite3
from sql_scripts import *


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('FIRM.db')
        self.c = self.conn.cursor()
        self.c.executescript(INIT_DB)
        self.conn.commit()

    def reg_employee(self, code, fio, position, number, mail):
        self.c.execute(INSERT_EMPLOYEE, (code, fio, position, number, mail))
        self.conn.commit()

    def reg_temp(self, code, fio, meta, number, mail, now_data=datetime.datetime.now().strftime('%d.%m.%Y')):
        self.c.execute(INSERT_VISITOR, (code, fio, meta, number, mail, now_data))
        self.conn.commit()

    def scan_employee(self, employee_id):
        data = datetime.datetime.now().strftime('%d.%m.%Y')
        time = datetime.datetime.now().strftime('%H:%M:%S')
        self.c.execute(COUNT_EMPLOYEES, (employee_id, data))
        res = int(self.c.fetchone()[0])
        if res % 2:
            self.c.execute(INSERT_VISIT, (employee_id, data, time, 'Отсутствует'))
        else:
            self.c.execute(INSERT_VISIT, (employee_id, data, time, 'Присутствует'))
        self.conn.commit()

    def scan_temp(self, visitor_id):
        data = datetime.datetime.now().strftime('%d.%m.%Y')
        time = datetime.datetime.now().strftime('%H:%M:%S')
        self.c.execute(COUNT_VISITORS, (data, visitor_id))
        res = int(self.c.fetchone()[0])
        if res % 2:
            self.c.execute(INSERT_TEMP, (visitor_id, time, 'Отсутствует'))
        else:
            self.c.execute(INSERT_TEMP, (visitor_id, time, 'Присутствует'))
        self.conn.commit()

    def check(self, employee_id):
        self.c.execute(CHECK_EMPL, (employee_id,))
        res = self.c.fetchall()
        self.conn.commit()
        if res:
            del res
            return True
        else:
            del res
            return False

    def check_temp(self, visitor_id):
        self.c.execute(CHECK_TEMP, (visitor_id,))
        res = self.c.fetchall()
        self.conn.commit()
        if res:
            del res
            return True
        else:
            del res
            return False

    def find_employees_status(self, status, now=datetime.datetime.now().strftime('%d.%m.%Y')):
        self.c.execute(EMPLOYEE_CUR_DATE, (status, now))
        self.conn.commit()
        lst = self.c.fetchall()
        return lst

    def find_employees(self):
        now = datetime.datetime.now().strftime('%d.%m.%Y')
        self.c.execute(EMPLOYEE_CUR_DATE, (now,))
        self.conn.commit()
        lst = self.c.fetchall()

        return lst

    def find_visitors_date(self):
        now = datetime.datetime.now().strftime('%d.%m.%Y')
        self.c.execute(VISITOR_CUR_DATE, (now,))
        self.conn.commit()
        lst = self.c.fetchall()
        return lst

    def find_all_employees(self):
        self.c.execute(EMPLOYEE_LIST)
        self.conn.commit()
        lst = self.c.fetchall()

        return lst
