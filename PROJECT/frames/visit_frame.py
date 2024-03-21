from tkinter import *
from tkinter.ttk import Treeview, Notebook
from PROJECT.database import DataBase


class VisitFrame(Frame):
    def __init__(self, parent):
        super(VisitFrame, self).__init__()
        self.parent = parent
        self.db = DataBase()

        notebook = Notebook(self)
        notebook.pack(pady=10, expand=True)

        button_prev = Button(self, text='Назад', width=20,
                             command=self.parent.set_main)

        frame_1 = Frame(notebook)
        frame_2 = Frame(notebook)

        notebook.add(frame_1, text='Присутствуют')
        notebook.add(frame_2, text='Отсутствуют')

        self.employee_tree = Treeview(frame_1, columns=('fullname', 'phone', 'email'), height=10, show='headings')
        self.employee_tree.heading('fullname', text='ФИО')
        self.employee_tree.heading('phone', text='Телефон')
        self.employee_tree.heading('email', text='Email')

        self.visitor_tree = Treeview(frame_1, columns=('fullname', 'phone', 'email'), height=10, show='headings')
        self.visitor_tree.heading('fullname', text='ФИО')
        self.visitor_tree.heading('phone', text='Телефон')
        self.visitor_tree.heading('email', text='email')

        label_emp = Label(frame_1, text='Сотрудники')
        label_vis = Label(frame_1, text='Посетители')

        button_prev.pack()
        label_emp.pack()
        self.employee_tree.pack()
        label_vis.pack()
        self.visitor_tree.pack()

        self.employee_tree_2 = Treeview(frame_2, columns=('fullname', 'phone', 'email'), height=10, show='headings')
        self.employee_tree_2.heading('fullname', text='ФИО')
        self.employee_tree_2.heading('phone', text='Телефон')
        self.employee_tree_2.heading('email', text='Email')

        self.visitor_tree_2 = Treeview(frame_2, columns=('fullname', 'phone', 'email'), height=10, show='headings')
        self.visitor_tree_2.heading('fullname', text='ФИО')
        self.visitor_tree_2.heading('phone', text='Телефон')
        self.visitor_tree_2.heading('email', text='email')

        label_emp = Label(frame_2, text='Работники')
        label_vis = Label(frame_2, text='Посетители')

        self.fill_tables(self.employee_tree, self.employee_tree_2)
        self.fill_tables(self.visitor_tree, self.visitor_tree_2, 2)
        label_emp.pack()
        self.employee_tree_2.pack()
        label_vis.pack()
        self.visitor_tree_2.pack()

        self.pack()

    def fill_tables(self, table_here, table_absent, who=1):
        list_users = self.db.find_users(who)

        if list_users is not None:
            for user in list_users:
                if user[4] == 0:
                    table_absent.insert('', 'end', iid=user[0], values=user[1:4])
                else:
                    table_here.insert('', 'end', iid=user[0], values=user[1:4])
