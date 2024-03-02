from tkinter import *
from tkinter.ttk import Treeview, Notebook
from PROJECT.database import DataBase


class VisitFrame(Frame):
    def __init__(self, parent):
        super(VisitFrame, self).__init__()
        self.parent = parent
        self.db = DataBase()
        # create a notebook
        notebook = Notebook(self)
        notebook.pack(pady=10, expand=True)

        button_prev = Button(self, text="Назад", width=20,
                             command=self.parent.set_main)
        # create frames
        frame_1 = Frame(notebook)
        frame_2 = Frame(notebook)

        # add frames to notebook

        notebook.add(frame_1, text='Присутствуют')
        notebook.add(frame_2, text='Отсутствуют')

        self.employee_tree = Treeview(frame_1, columns=('fullname', 'phone', 'position'), height=10, show='headings')
        self.employee_tree.heading('fullname', text='ФИО')
        self.employee_tree.heading('phone', text='Телефон')
        self.employee_tree.heading('position', text='Должность')

        self.visitor_tree = Treeview(frame_1, columns=('fullname', 'phone', 'meta'), height=10, show='headings')
        self.visitor_tree.heading('fullname', text='ФИО')
        self.visitor_tree.heading('phone', text='Телефон')
        self.visitor_tree.heading('meta', text='Цель')

        label_emp = Label(frame_1, text='Работники')
        label_vis = Label(frame_1, text='Гости')

        button_prev.pack()
        label_emp.pack()
        self.employee_tree.pack()
        label_vis.pack()
        self.visitor_tree.pack()

        self.employee_tree_2 = Treeview(frame_2, columns=('fullname', 'phone', 'position'), height=10, show='headings')
        self.employee_tree_2.heading('fullname', text='ФИО')
        self.employee_tree_2.heading('phone', text='Телефон')
        self.employee_tree_2.heading('position', text='Должность')

        self.visitor_tree_2 = Treeview(frame_2, columns=('fullname', 'phone', 'meta'), height=10, show='headings')
        self.visitor_tree_2.heading('fullname', text='ФИО')
        self.visitor_tree_2.heading('phone', text='Телефон')
        self.visitor_tree_2.heading('meta', text='Цель')

        label_emp = Label(frame_2, text='Работники')
        label_vis = Label(frame_2, text='Гости')

        label_emp.pack()
        self.employee_tree_2.pack()
        label_vis.pack()
        self.visitor_tree_2.pack()

        self.pack()

    def fill_table(self, table, state='Присутствует', who='Сотрудник'):
        if who == 'Сотрудник':
            l_emp = self.db.find_employees()
            for i, value in enumerate(l_emp):
                if value[4] == state:
                    table.insert("", 'end', iid=i,
                                 values=value[:4])
        else:
            l_emp = self.db.find_visitors_date()
            for i, value in enumerate(l_emp):
                if value[4] == state:
                    table.insert("", 'end', iid=i,
                                 values=value[:4])
