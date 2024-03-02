import asyncio
import os
import pyqrcode
import tkinter.messagebox

# from PROJECT.mail import send_mail
# from PROJECT.consts import RECEIVER

from PROJECT.database import DataBase
from tkinter import *


async def make_qr(data_string, path='/employee/'):
    if not os.path.exists(os.getcwd() + path):
        os.makedirs(os.getcwd() + path)

    generated_qr = pyqrcode.create(data_string, error='Q', version=5, encoding='utf-8')
    generated_qr.png(os.getcwd() + path + '\\qr.png', scale=7)
    
    # ! add to database


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

        button_scan = Button(self, text="Сканирование", width=30, command=self.parent.set_scanner)
        button_scan.grid(column=0, row=1, padx=5, pady=5)

        button_audit = Button(self, text="Сотрудники | Посетители", width=30, command=self.parent.set_visit)
        button_audit.grid(column=0, row=2, padx=5, pady=5)

        button_reg = Button(self, text="Регистрация сотрудника", width=30, command=self.sign_in)
        button_reg.grid(column=0, row=3, padx=5, pady=5)

        button_pass = Button(self, text="Создать временный пропуск", width=30,
                             command=lambda: self.sign_in(is_employee=False))
        button_pass.grid(column=0, row=4, padx=5, pady=5)

        self.pack()

    def sign_in(self, is_employee=True):
        top_win = Toplevel()
        top_win.geometry('400x300+100+100')
        top_win.columnconfigure(2, weight=1)
        top_win.rowconfigure(7, weight=1)

        surname = StringVar()
        name = StringVar()
        patronymic = StringVar()
        phone = StringVar()
        occupation = StringVar()
        meta = StringVar()
        mail = StringVar()

        label_surname: Label = Label(top_win, text='Фамилия')
        label_name: Label = Label(top_win, text='Имя')
        label_patronymic: Label = Label(top_win, text='Отчество')
        label_phone: Label = Label(top_win, text='Телефон')
        label_mail: Label = Label(top_win, text='E-mail')
        label_occupation: Label = Label(top_win, text='Должность')
        label_meta: Label = Label(top_win, text='Цель визита')

        # ! нет валидации на полях
        entry_surname = Entry(top_win, textvariable=surname)
        entry_name = Entry(top_win, textvariable=name)
        entry_patronymic = Entry(top_win, textvariable=patronymic)
        entry_phone = Entry(top_win, textvariable=phone)
        entry_occupation = Entry(top_win, textvariable=occupation)
        entry_meta = Entry(top_win, textvariable=meta)
        entry_mail = Entry(top_win, textvariable=mail)

        if is_employee:
            top_win.wm_title("Регистрация сотрудника")
            button_close: Button = Button(top_win, text="Отменить", command=top_win.destroy)
            button_register: Button = Button(top_win, text="Зарегистрировать",
                                             command=lambda: self.create_entry(surname=surname.get(), name=name.get(),
                                                                               patronymic=patronymic.get(),
                                                                               occup=occupation.get(),
                                                                               phone=phone.get(),
                                                                               email=mail.get(), meta=meta.get(),
                                                                               window=top_win))

            label_surname.grid(row=0, column=0, padx=5, pady=5)
            label_name.grid(row=1, column=0, padx=5, pady=5)
            label_patronymic.grid(row=2, column=0, padx=5, pady=5)
            label_occupation.grid(row=3, column=0, padx=5, pady=5)
            label_phone.grid(row=4, column=0, padx=5, pady=5)
            label_mail.grid(row=5, column=0, padx=5, pady=5)

            entry_surname.grid(row=0, column=1, padx=5, pady=5)
            entry_name.grid(row=1, column=1, padx=5, pady=5)
            entry_patronymic.grid(row=2, column=1, padx=5, pady=5)
            entry_occupation.grid(row=3, column=1, padx=5, pady=5)
            entry_phone.grid(row=4, column=1, padx=5, pady=5)
            entry_mail.grid(row=5, column=1, padx=5, pady=5)
            button_register.grid(row=6, column=1, padx=5, pady=5)
            button_close.grid(row=6, column=0, padx=5, pady=5)
            button_register.grid(row=6, column=1, padx=5, pady=5)
            button_close.grid(row=6, column=0, padx=5, pady=5)

            top_win.grab_set()
            top_win.attributes('-topmost', 'true')

        else:
            top_win.wm_title("Временный пропуск")

            button_close = Button(top_win, text="Отменить", command=top_win.destroy)
            button_register = Button(top_win, text="Зарегистрировать",
                                     command=lambda: self.create_entry(surname=surname.get(), name=name.get(),
                                                                       patronymic=patronymic.get(), occup=occupation.get(),
                                                                       phone=phone.get(),
                                                                       email=mail.get(), meta=meta.get(),
                                                                       window=top_win))

            label_surname.grid(row=0, column=0, padx=5, pady=5)
            label_name.grid(row=1, column=0, padx=5, pady=5)
            label_patronymic.grid(row=2, column=0, padx=5, pady=5)
            label_meta.grid(row=3, column=0, padx=5, pady=5)
            label_phone.grid(row=4, column=0, padx=5, pady=5)
            label_mail.grid(row=5, column=0, padx=5, pady=5)

            entry_surname.grid(row=0, column=1, padx=5, pady=5)
            entry_name.grid(row=1, column=1, padx=5, pady=5)
            entry_patronymic.grid(row=2, column=1, padx=5, pady=5)
            entry_meta.grid(row=3, column=1, padx=5, pady=5)
            entry_phone.grid(row=4, column=1, padx=5, pady=5)
            entry_mail.grid(row=5, column=1, padx=5, pady=5)
            button_register.grid(row=6, column=1, padx=5, pady=5)
            button_close.grid(row=6, column=0, padx=5, pady=5)

            top_win.grab_set()
            top_win.attributes('-topmost', 'true')

    def create_entry(self, surname, name, patronymic, occup, phone, email, meta, window):
        fullname = f'{surname} {name} {patronymic}'
        import random
        id_emp = email + '' + str(random.randint(1, 100))

        if occup:
            try:
                if surname and name and patronymic and phone and email:
                    self.db.reg_employee(id_emp, fullname, occup, phone, email)
                    asyncio.get_event_loop().run_until_complete(make_qr(id_emp, path='\\PROJECT\\passes\\employee\\' + email))

                    # asyncio.get_event_loop().run_until_complete(send_mail(RECIEVER, path=r'/employee/' + email))
                    # ! Edit messagebox
                    tkinter.messagebox.showinfo('Регистрация сотрудника', 'QR создан и отправлен на указанную почту!')
                    window.destroy()
                else:
                    tkinter.messagebox.showwarning('Регистрация сотрудника', 'Не все поля заполены!')

            except Exception as e:
                print(e)
                tkinter.messagebox.showerror('Регистрация сотрудника',
                                             'QR не был создан, проверьте корректность введенных данных!')
        else:
            try:
                if surname and name and patronymic and phone and email and meta:
                    self.db.reg_temp(id_emp, fullname, meta, phone, email)
                    asyncio.get_event_loop().run_until_complete(make_qr(id_emp, path='\\PROJECT\\passes\\temporary\\' + email))

                    # asyncio.get_event_loop().run_until_complete(send_mail(RECIEVER, path=r'/temporary/' + email))
                    # ! Edit messagebox
                    tkinter.messagebox.showinfo('Временный пропуск', 'QR создан и отправлен на указанную почту!', )
                    window.destroy()
                else:
                    tkinter.messagebox.showwarning('Временный пропуск', 'Не все поля заполены!')

            except Exception as e:
                print(e)
                tkinter.messagebox.showerror('Временный пропуск',
                                             'QR не был создан, проверьте корректность введенных данных!')
