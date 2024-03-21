import os
import tkinter

import pyqrcode
import tkinter.messagebox
import random
from PROJECT.database import DataBase
from tkinter import *


# from PROJECT.mail import send_mail
# from PROJECT.consts import RECEIVER


def make_qr(data_string, path='/employee/'):
    if not os.path.exists(os.getcwd() + path):
        os.makedirs(os.getcwd() + path)

    generated_qr = pyqrcode.create(data_string, error='Q', version=5, encoding='utf-8')
    try:
        generated_qr.png(os.getcwd() + path + '\\qr.png', scale=7)
        return True
    except Exception:
        return False


class MainFrame(Frame):
    def __init__(self, parent):
        super(MainFrame, self).__init__()
        self.parent = parent
        self.db = DataBase()

        self.columnconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)

        self.img_logo = PhotoImage(file=os.getcwd() + '\\PROJECT\\img\\logo.png')

        label_logo = Label(self, image=self.img_logo)

        label_logo.grid(column=0, row=0, padx=5, pady=5)

        button_scan = Button(self, text='Сканирование', width=30, command=self.parent.set_scanner)
        button_scan.grid(column=0, row=1, padx=5, pady=5)

        button_audit = Button(self, text='Статус на объекте', width=30, command=self.parent.set_visit)
        button_audit.grid(column=0, row=2, padx=5, pady=5)

        button_reg = Button(self, text='Создание пропуска', width=30, command=self.sign_in)
        button_reg.grid(column=0, row=3, padx=5, pady=5)

        self.pack()

    def sign_in(self):
        top_win = Toplevel()
        top_win.geometry('350x250+100+100')
        top_win.columnconfigure(2, weight=1)
        top_win.rowconfigure(7, weight=1)
        top_win.resizable(False, False)

        surname = StringVar()
        name = StringVar()
        patronymic = StringVar()
        phone = StringVar()
        mail = StringVar()

        label_surname: Label = Label(top_win, text='Фамилия')
        label_name: Label = Label(top_win, text='Имя')
        label_patronymic: Label = Label(top_win, text='Отчество')
        label_phone: Label = Label(top_win, text='Телефон')
        label_mail: Label = Label(top_win, text='E-mail')

        # ! нет валидации на полях
        entry_surname = Entry(top_win, textvariable=surname)
        entry_name = Entry(top_win, textvariable=name)
        entry_patronymic = Entry(top_win, textvariable=patronymic)
        entry_phone = Entry(top_win, textvariable=phone)
        entry_mail = Entry(top_win, textvariable=mail)
        user_type = tkinter.IntVar()
        check_type = Checkbutton(top_win, text='Является посетителем?', onvalue=1, variable=user_type)

        top_win.wm_title("Регистрация сотрудника")
        button_close: Button = Button(top_win, text="Отменить", command=top_win.destroy)
        button_register: Button = Button(top_win, text="Зарегистрировать",
                                         command=lambda: self.create_entry(surname=surname.get(), name=name.get(),
                                                                           patronymic=patronymic.get(),
                                                                           user_type=user_type.get() + 1,
                                                                           phone=phone.get(),
                                                                           email=mail.get(),
                                                                           window=top_win))

        label_surname.grid(row=0, column=0, padx=5, pady=5)
        label_name.grid(row=1, column=0, padx=5, pady=5)
        label_patronymic.grid(row=2, column=0, padx=5, pady=5)
        label_phone.grid(row=3, column=0, padx=5, pady=5)
        label_mail.grid(row=4, column=0, padx=5, pady=5)
        check_type.grid(row=5, column=0, padx=5, pady=5)

        entry_surname.grid(row=0, column=1, padx=5, pady=5)
        entry_name.grid(row=1, column=1, padx=5, pady=5)
        entry_patronymic.grid(row=2, column=1, padx=5, pady=5)
        entry_phone.grid(row=3, column=1, padx=5, pady=5)
        entry_mail.grid(row=4, column=1, padx=5, pady=5)

        button_register.grid(row=6, column=1, padx=5, pady=5)
        button_close.grid(row=6, column=0, padx=5, pady=5)
        button_register.grid(row=6, column=1, padx=5, pady=5)
        button_close.grid(row=6, column=0, padx=5, pady=5)

        top_win.grab_set()
        top_win.attributes('-topmost', 'true')

    @staticmethod
    def validate_email(value):
        import re
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value) is None:
            return False

        return True

    @staticmethod
    def validate_phone(value):
        if value.isdigit() is False and len(value) != 11:
            return False

        return True

    def create_entry(self, surname, name, patronymic, user_type, phone, email, window):
        fullname = f'{surname} {name} {patronymic}'
        id_emp = email + '' + str(random.randint(1, 1000))

        if user_type == 1:
            path = '\\PROJECT\\passes\\employee\\' + email
        else:
            path = '\\PROJECT\\passes\\temporary\\' + email

        if surname and name and patronymic and self.validate_phone(phone) and self.validate_email(email):
            result = make_qr(id_emp, path=path)
            if result:
                self.db.register_user(id_emp, fullname, user_type, phone, email)
                tkinter.messagebox.showinfo('Регистрация завершена',
                                            'QR создан и отправлен на указанную почту!')
                window.destroy()
            else:
                tkinter.messagebox.showwarning('Ошибка генерации QR-кода', 'QR-код не был создан!')
        else:
            tkinter.messagebox.showwarning('Регистрация не завершена', 'Проверьте корректность вводимых данных!')


