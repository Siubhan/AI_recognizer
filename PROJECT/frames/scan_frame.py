import os
import cv2

from tkinter import *
from tkinter import messagebox


class ScanFrame(Frame):
    def __init__(self, parent):
        super(ScanFrame, self).__init__()
        self.parent = parent

        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)
        self.img_scan = PhotoImage(file=os.getcwd() + '\\PROJECT\\img\\scan.png')

        label_scan = Label(self, image=self.img_scan)

        button_scan = Button(self, text='Сканировать', width=20,
                             command=self.scan)

        button_prev = Button(self, text='Назад', width=20,
                             command=self.parent.set_main)

        button_prev.grid(column=0, row=0, padx=5, pady=5)
        label_scan.grid(column=0, row=1, padx=5, pady=5)
        button_scan.grid(column=0, row=2, padx=5, pady=5)
        self.pack()

    def scan(self):
        delay = 1
        window_name = 'OpenCV Scanner'

        bd = cv2.QRCodeDetector()
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            # cv2.imshow(window_name, frame)

            key = cv2.waitKey(delay) & 0xFF

            if key == ord('q'):
                break

            if ret:
                decoded_info, points, straight_qrcode = bd.detectAndDecode(frame)

                if points is not None and decoded_info is not None:
                    if decoded_info:
                        self.parent.db.scan_employee(decoded_info)
                        messagebox.showwarning('Пропуск корректен',
                                               'Пропуск успешно распознан!')
                        break
                    # else:
                    #     messagebox.showwarning('Некорректный QR-пропуск',
                    #                            'Сканированный QR код в базе данных отсутствует!')

        # cv2.destroyWindow(window_name)
        cap.release()
