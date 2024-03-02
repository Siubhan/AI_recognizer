import wx

from database import DataBase
from style import *


class Tab(wx.Panel):
    def __init__(self, parent, tab_type=0):
        wx.Panel.__init__(self, parent)

        self.db = DataBase()

        self.width, self.height, font_size = get_measurement()
        self.font = wx.Font(wx.FontInfo(font_size))

        vert = wx.BoxSizer(wx.VERTICAL)
        horizontal = wx.BoxSizer(wx.HORIZONTAL)

        l1 = wx.StaticText(self, label='Сотрудники')
        l2 = wx.StaticText(self, label='Посетители')

        self.list_workers = wx.ListCtrl(self, -1, size=(self.width, self.height // 3),
                                        style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_workers.InsertColumn(0, 'ФИО', width=self.width // 4)
        self.list_workers.InsertColumn(1, 'Должность', width=self.width // 4)
        self.list_workers.InsertColumn(2, 'Номер телефона', width=self.width // 4)
        self.list_workers.InsertColumn(3, 'Час прибытия', width=self.width / 4.8)

        self.list_visitors = wx.ListCtrl(self, -1, size=(self.width, self.height // 3),
                                         style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_visitors.InsertColumn(0, 'ФИО', width=self.width / 4)
        self.list_visitors.InsertColumn(1, 'Цель визита', width=self.width / 4)
        self.list_visitors.InsertColumn(2, 'Номер телефона', width=self.width / 4)
        self.list_visitors.InsertColumn(3, 'Час прибытия', width=self.width / 4.8)
        vert.Add(l1, 1, wx.ALL | wx.CENTER, 5)

        vert.Add(self.list_workers, 1, wx.ALL | wx.CENTER, 5)
        vert.Add(l2, 1, wx.ALL | wx.CENTER, 5)

        vert.Add(self.list_visitors, 1, wx.ALL | wx.CENTER, 5)
        vert.Add((0, 0), 1, wx.EXPAND | wx.ALL | wx.CENTER, 5)
        vert.Add((0, 0), 1, wx.EXPAND | wx.ALL | wx.CENTER, 5)
        horizontal.Add(vert, 1, wx.ALL | wx.CENTER, 5)
        if tab_type == 0:
            self.fill_table()
            self.fill_table(who='Гость')
        else:
            self.fill_table(state='Нет')
            self.fill_table(state='Нет', who='Гость')

        self.SetSizer(horizontal)
        self.Layout()

    def fill_table(self, state='Присутствует', who='Сотрудник'):
        if who == 'Сотрудник':
            l_emp = self.db.find_employees()
            for i, value in enumerate(l_emp):
                if value[4] == state:
                    self.list_workers.Append(value[:4])
        else:
            l_emp = self.db.find_visitors_date()
            for i, value in enumerate(l_emp):
                if value[4] == state:
                    self.list_visitors.Append(value[:4])
