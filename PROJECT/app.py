from tkinter import *

from database import DataBase

from frames.main_frame import MainFrame
from frames.scan_frame import ScanFrame
from frames.visit_frame import VisitFrame


class Interface(Tk):
    def __init__(self):
        super(Interface, self).__init__()
        self.title("Alternative")
        self.geometry('800x600')

        self.db = DataBase()
        self.current_frame = MainFrame(self)
        self.current_frame.pack()

    def set_visit(self):
        new_frame = VisitFrame(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

    def set_scanner(self):
        new_frame = ScanFrame(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

    def set_main(self):
        new_frame = MainFrame(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()


if __name__ == '__main__':
    app = Interface()
    app.mainloop()
