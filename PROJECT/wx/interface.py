import os
import asyncio

import wx

from scanner import Scanner
from database import DataBase
from registration import Registration
from tab import Tab
from style import *


class Interface(wx.Frame):
    def __init__(self, *arg, **kwargs):
        super(Interface, self).__init__(*arg, **kwargs)
        self.button_scan = None
        self.SetTitle('Alternative')
        self.width, self.height, font_size = get_measurement()
        self.font = wx.Font(wx.FontInfo(font_size))

        self.db = DataBase()
        self.img_logo = wx.Image(os.getcwd() + '/img/logo.png', wx.BITMAP_TYPE_ANY)
        self.img_scanner = wx.Image(os.getcwd() + '/img/scan.png', wx.BITMAP_TYPE_ANY)

        self.general_panel = wx.Panel(parent=self)
        self.audit_panel = wx.Panel(parent=self)
        self.scan_panel = wx.Panel(parent=self)

        self.audit_panel.Hide()
        self.scan_panel.Hide()

        self.SetSize(0, 0, self.width, self.height)
        self.general_panel.SetSize(0, 0, self.width, self.height)
        self.audit_panel.SetSize(0, 0, self.width, self.height)
        self.scan_panel.SetSize(0, 0, self.width, self.height)

        self.set_general()

        self.Centre()
        self.Show(True)

    def set_general(self):
        self.general_panel.Show(True)
        self.audit_panel.Hide()
        self.scan_panel.Hide()

        sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridSizer(1, 5, 5, 5)

        logo = wx.StaticBitmap(self.general_panel, wx.ID_ANY, wx.Bitmap(self.img_logo))

        button_scan = wx.Button(self.general_panel, label='Сканирование', size=B_SIZE)
        button_audit = wx.Button(self.general_panel, label='Сотрудники | Посетители', size=B_SIZE)
        button_reg = wx.Button(self.general_panel, label='Регистрация', size=B_SIZE)
        button_pass = wx.Button(self.general_panel, label='Временный пропуск', size=B_SIZE)
        button_pass.name = 'пропуск'
        button_reg.name = 'регистрация'

        button_scan.Bind(wx.EVT_BUTTON, lambda e: self.set_scanner())
        button_audit.Bind(wx.EVT_BUTTON, lambda e: self.set_audit())
        button_reg.Bind(wx.EVT_BUTTON, self.set_registration)
        button_pass.Bind(wx.EVT_BUTTON, self.set_registration)

        button_scan.SetFont(self.font)
        button_audit.SetFont(self.font)
        button_reg.SetFont(self.font)
        button_pass.SetFont(self.font)

        grid.Add(logo, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=10)
        grid.Add(button_scan, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=10)
        grid.Add(button_reg, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=10)
        grid.Add(button_pass, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=10)
        grid.Add(button_audit, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=10)

        sizer.Add(grid, flag=wx.ALL, border=10)
        self.general_panel.SetSizer(sizer)

        self.Layout()


    def set_scanner(self):
        self.general_panel.Hide()
        self.scan_panel.Show(True)
        sizer = wx.BoxSizer()

        img = wx.StaticBitmap(self.scan_panel, wx.ID_ANY, wx.Bitmap(self.img_scanner))

        b = wx.Button(self.scan_panel, label='Назад')
        b.SetFont(self.font)
        button_scan = wx.Button(self.scan_panel, label='Сканировать')
        button_scan.SetFont(self.font)

        sizer.Add(b, 0, wx.ALL | wx.LEFT | wx.BOTTOM | wx.ALIGN_BOTTOM, 5)
        sizer.Add(img, 0, wx.CENTER | wx.ALL)
        sizer.Add(button_scan, 0, wx.ALL | wx.CENTER, 5)

        b.Bind(wx.EVT_BUTTON, lambda e: self.set_general())

        self.SetAutoLayout(sizer)
        self.Layout()
        self.Refresh()

        # self.button_scan.Bind(wx.EVT_BUTTON, lambda e: asyncio.get_event_loop().run_until_complete(self.turn_on()))

    async def turn_on(self):
        c = Scanner(self)
        # c.scan()

    def set_audit(self):
        self.general_panel.Hide()
        self.audit_panel.Show(True)
        hbox = wx.BoxSizer(wx.VERTICAL)

        nb = wx.Notebook(self.audit_panel)
        nb.AddPage(Tab(nb, 0), 'Присуствуют')
        nb.AddPage(Tab(nb, 1), 'Отсутствуют')

        b = wx.Button(self.audit_panel, label='Назад')
        b.SetFont(self.font)

        hbox.Add(b, 0, wx.ALL | wx.LEFT | wx.BOTTOM | wx.ALIGN_BOTTOM, 5)
        hbox.Add(nb, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        b.Bind(wx.EVT_BUTTON, lambda e: self.set_general())
        self.SetSizer(hbox)
        self.Layout()
        self.Refresh()

    def set_registration(self, event):
        if event.GetEventObject().name == 'регистрация':
            r = Registration(self)
        else:
            r = Registration(self, is_emp=1)
        r.ShowModal()
        r.Close()


if __name__ == '__main__':
    app = wx.App()
    Interface(None, style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX)
    app.MainLoop()
