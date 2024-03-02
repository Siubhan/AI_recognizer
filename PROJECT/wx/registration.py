import asyncio
import os
import pyqrcode
import wx
import wx.adv
import wx.lib.masked
import datetime
import locale
from mail import send_mail
from style import *
from consts import RECIEVER


class Registration(wx.Dialog):
    def __init__(self, parent, is_emp=0):
        super(Registration, self).__init__(parent)

        self.phone = None
        self.email = None
        self.position = None
        self.patronymic = None
        self.name = None
        self.surname = None
        self.contract_date = None
        self.contract_no = None
        self.meta = None

        locale.setlocale(locale.LC_ALL, '')

        self.width, self.height, font_size = get_measurement()
        self.font = wx.Font(wx.FontInfo(font_size))
        self.SetSize(0, 0, self.width, self.height)
        if not is_emp:
            self.init_worker()
        else:
            self.init_temp()

    def init_worker(self):
        pnl = wx.Panel(parent=self)
        pnl.SetSize(self.width, self.height)
        title = wx.StaticText(pnl, label='Регистрация сотрудника')
        sizer = wx.GridSizer(9, 3, 0, 0)

        hor = wx.BoxSizer(wx.HORIZONTAL)
        hor2 = wx.BoxSizer(wx.HORIZONTAL)
        ver = wx.BoxSizer(wx.VERTICAL)

        btn_reg = wx.Button(pnl, label='Зарегистрировать', size=B_SIZE)
        btn_cnl = wx.Button(pnl, label='Отменить', size=B_SIZE)
        btn_cnl.Bind(wx.EVT_BUTTON, lambda e: self.close())
        btn_reg.Bind(wx.EVT_BUTTON, lambda e: self.reg_worker())

        l1 = wx.StaticText(pnl, label='Фамилия')
        l2 = wx.StaticText(pnl, label='Имя')
        l3 = wx.StaticText(pnl, label='Отчество')
        l6 = wx.StaticText(pnl, label='Трудовой договор')
        l7 = wx.StaticText(pnl, label='Номер')
        l8 = wx.StaticText(pnl, label='Дата')
        l9 = wx.StaticText(pnl, label='Должность')
        l10 = wx.StaticText(pnl, label='Телефон')
        l11 = wx.StaticText(pnl, label='E-mail')

        choises = ['Дизайнер', 'Директор', 'Бухгалтер', 'Экономист', 'Программист', 'Менеджер']

        self.contract_no = wx.TextCtrl(pnl, size=B_SIZE)
        self.contract_date = wx.adv.DatePickerCtrl(pnl, size=B_SIZE, dt=wx.DateTime(datetime.datetime.now()))

        self.surname = wx.TextCtrl(pnl, size=B_SIZE)
        self.name = wx.TextCtrl(pnl, size=B_SIZE)
        self.patronymic = wx.TextCtrl(pnl, size=B_SIZE)

        self.position = wx.ComboBox(pnl, value=choises[0], choices=choises, style=wx.CB_READONLY, size=B_SIZE)
        self.phone = wx.lib.masked.TextCtrl(pnl, size=B_SIZE, mask='(###)###-####')
        self.email = wx.TextCtrl(pnl, size=B_SIZE)

        self.contract_no.Bind(wx.EVT_CHAR, lambda e: is_digit(e))
        self.contract_date.Bind(wx.EVT_CHAR, lambda e: is_digit(e))
        self.surname.Bind(wx.EVT_CHAR, lambda e: is_char(e))
        self.name.Bind(wx.EVT_CHAR, lambda e: is_char(e))
        self.patronymic.Bind(wx.EVT_CHAR, lambda e: is_char(e))
        self.position.Bind(wx.EVT_CHAR, lambda e: is_char(e))
        self.email.Bind(wx.EVT_CHAR, lambda e: is_mail(e))

        sizer.Add((0, 0), wx.ALL)
        sizer.Add(title, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer.Add((0, 0), wx.ALL)

        sizer.Add(l6, 0, wx.ALL | wx.ALIGN_BOTTOM, 0)
        sizer.Add((0, 0), wx.ALL)
        sizer.Add((0, 0), wx.ALL)

        sizer.Add(l7, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.CENTER, 5)
        sizer.Add(l8, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.CENTER, 5)
        sizer.Add((0, 0), wx.ALL)

        sizer.Add(self.contract_no, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.contract_date, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add((0, 0), wx.ALL)

        sizer.Add(l1, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.CENTER, 5)
        sizer.Add(l2, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.CENTER, 5)
        sizer.Add(l3, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.CENTER, 5)

        sizer.Add(self.surname, 0, wx.ALL, 10)
        sizer.Add(self.name, 0, wx.ALL, 10)
        sizer.Add(self.patronymic, 0, wx.ALL, 10)

        sizer.Add(l9, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)
        sizer.Add(l10, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)
        sizer.Add(l11, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)

        sizer.Add(self.position, 0, wx.ALL, 10)
        sizer.Add(self.phone, 0, wx.ALL, 10)
        sizer.Add(self.email, 0, wx.ALL, 10)

        hor2.Add(btn_cnl, 0, wx.ALL | wx.ALIGN_RIGHT, 40)
        hor2.Add((0, 0), wx.ALL)
        hor2.Add((0, 0), wx.ALL)
        hor2.Add(btn_reg, 0, wx.ALL | wx.ALIGN_RIGHT, 40)

        ver.Add(sizer, 1, wx.CENTER | wx.ALL | wx.ALIGN_TOP | wx.ALIGN_CENTER_HORIZONTAL)
        ver.Add(hor2, 1, wx.CENTER | wx.ALL | wx.ALIGN_TOP | wx.ALIGN_CENTER_HORIZONTAL)
        hor.Add(ver, 1, wx.ALL | wx.CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)

        self.SetSizer(hor)
        self.Layout()

    def init_temp(self):
        pnl = wx.Panel(self)
        pnl.SetSize(self.width, self.height)

        title = wx.StaticText(pnl, label='Однодневный пропуск')
        sizer = wx.GridSizer(6, 3, 0, 0)

        hor = wx.BoxSizer(wx.HORIZONTAL)
        hor2 = wx.BoxSizer(wx.HORIZONTAL)
        ver = wx.BoxSizer(wx.VERTICAL)

        btn_reg = wx.Button(pnl, label='Зарегистрировать', size=B_SIZE)
        btn_cnl = wx.Button(pnl, label='Отменить', size=B_SIZE)
        btn_cnl.Bind(wx.EVT_BUTTON, lambda e: self.close())
        btn_reg.Bind(wx.EVT_BUTTON, lambda e: self.reg_visitor())

        l1 = wx.StaticText(pnl, label='Фамилия')
        l2 = wx.StaticText(pnl, label='Имя')
        l3 = wx.StaticText(pnl, label='Отчество')
        l6 = wx.StaticText(pnl, label='Цель визита')
        l10 = wx.StaticText(pnl, label='Телефон')
        l11 = wx.StaticText(pnl, label='E-mail')

        self.surname = wx.TextCtrl(pnl, size=B_SIZE)
        self.name = wx.TextCtrl(pnl, size=B_SIZE)
        self.patronymic = wx.TextCtrl(pnl, size=B_SIZE)
        self.meta = wx.TextCtrl(pnl, size=B_SIZE)
        self.phone = wx.lib.masked.TextCtrl(pnl, size=B_SIZE, mask='(###)###-####')
        self.email = wx.TextCtrl(pnl, size=B_SIZE)

        self.meta.Bind(wx.EVT_CHAR, lambda e: is_char(e))
        self.surname.Bind(wx.EVT_CHAR, lambda e: is_char(e))
        self.name.Bind(wx.EVT_CHAR, lambda e: is_char(e))
        self.patronymic.Bind(wx.EVT_CHAR, lambda e: is_char(e))
        self.email.Bind(wx.EVT_CHAR, lambda e: is_mail(e))

        sizer.Add((0, 0), wx.ALL)
        sizer.Add(title, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer.Add((0, 0), wx.ALL)

        sizer.Add(l1, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.CENTER, 5)
        sizer.Add(l2, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.CENTER, 5)
        sizer.Add(l3, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.CENTER, 5)

        sizer.Add(self.surname, 0, wx.ALL, 10)
        sizer.Add(self.name, 0, wx.ALL, 10)
        sizer.Add(self.patronymic, 0, wx.ALL, 10)

        sizer.Add(l6, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)
        sizer.Add(l10, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)
        sizer.Add(l11, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)

        sizer.Add(self.meta, 0, wx.ALL, 10)
        sizer.Add(self.phone, 0, wx.ALL, 10)
        sizer.Add(self.email, 0, wx.ALL, 10)

        hor2.Add(btn_cnl, 0, wx.ALL | wx.ALIGN_RIGHT, 40)
        hor2.Add((0, 0), wx.ALL)
        hor2.Add((0, 0), wx.ALL)
        hor2.Add(btn_reg, 0, wx.ALL | wx.ALIGN_RIGHT, 40)

        ver.Add(sizer, 1, wx.CENTER | wx.ALL | wx.ALIGN_TOP | wx.ALIGN_CENTER_HORIZONTAL)
        ver.Add(hor2, 1, wx.CENTER | wx.ALL | wx.ALIGN_TOP | wx.ALIGN_CENTER_HORIZONTAL)
        hor.Add(ver, 1, wx.ALL | wx.CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)

        pnl.SetSizer(hor)
        self.Layout()

    def close(self):
        self.Close()
        self.Destroy()

    def reg_worker(self):
        import random
        id_emp = self.email.GetValue() + '' + str(random.randint(10, 100))
        fio = self.surname.GetValue() + ' ' + self.name.GetValue() + ' ' + self.patronymic.GetValue()
        nmdg = self.contract_no.GetValue()
        dtdg = self.contract_date.GetValue()
        dtdg = dtdg.Format("%d.%m.%Y")
        dlgn = self.position.GetValue()
        ntel = self.phone.GetValue()
        mail = self.email.GetValue()

        try:
            if fio and nmdg and dtdg and dlgn and ntel and mail:
                self.Parent.db.reg_employee(id_emp, nmdg, dtdg, fio, dlgn, ntel, mail)
                asyncio.get_event_loop().run_until_complete(make_qr(id_emp, path=r'/employee/' + mail))

                asyncio.get_event_loop().run_until_complete(send_mail(RECIEVER, mail))

                wx.MessageBox('QR создан и отправлен на указанную почту!', 'Регистрация сотрудника',
                              wx.OK | wx.ICON_INFORMATION)
                self.Close()
                self.Destroy()
            else:
                wx.MessageBox('Не все поля заполены!', 'Регистрация сотрудника',
                              wx.OK | wx.ICON_ERROR)

        except Exception as e:
            print(e)
            wx.MessageBox('QR не был создан, проверьте корректность введенных данных!', 'Регистрация сотрудника',
                          wx.OK | wx.ICON_ERROR)

    def reg_visitor(self):
        fio = self.surname.GetValue() + ' ' + self.name.GetValue() + ' ' + self.patronymic.GetValue()
        meta = self.meta.GetValue()
        dt = datetime.datetime.now().strftime('%d.%m.%Y')
        ntel = self.phone.GetValue()
        mail = self.email.GetValue()
        import random
        id_emp = self.email.GetValue() + '' + str(random.randint(10, 100)) + ''.join(dt.split('.'))
        try:
            if fio and dt and meta and ntel and mail:
                self.Parent.db.reg_temp(id_emp, fio, meta, ntel, mail)

                asyncio.get_event_loop().run_until_complete(make_qr(id_emp, path=r'/tempQR/' + mail))

                asyncio.get_event_loop().run_until_complete(send_mail(RECIEVER, mail))

                wx.MessageBox('QR создан и отправлен на указанную почту!', 'Регистрация сотрудника',
                              wx.OK | wx.ICON_INFORMATION)
                self.Close()
                self.Destroy()
            else:
                wx.MessageBox('Не все поля заполены!', 'Регистрация сотрудника',
                              wx.OK | wx.ICON_ERROR)

        except Exception as e:
            print(e)
            wx.MessageBox('QR не был создан, проверьте корректность введенных данных!', 'Регистрация сотрудника',
                          wx.OK | wx.ICON_ERROR)



