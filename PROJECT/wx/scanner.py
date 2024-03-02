import cv2
# from qreader import QReader
import wx
import sql_scripts


class Scanner:
    def __init__(self, parent):
        self.parent = parent
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 300)
        self.text = ''

    # def scan(self):
    #     try:
    #         detector = cv2.QRCodeDetector()
    #         # _, frame = self.cam.read()
    #         # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         # frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #         #                               cv2.THRESH_BINARY, 11, 5)
    #
    #         # qrcodes = QReader.detect_and_decode(frame)
    #         key = cv2.waitKey(1)
    #         if key == ord('q'):
    #             self.cam.release()
    #             cv2.destroyAllWindows()
    #         else:
    #             cv2.imshow("Scanner", frame)
    #
    #             if qrcodes is not None:
    #                 for qrcode in qrcodes:
    #                     qrcode_data = qrcode.data.decode("utf-8")
    #                     qrcode_type = qrcode.type
    #
    #                     self.text = "{} ({})".format(qrcode_data, qrcode_type)
    #                     if self.parent.db.check(qrcode_data):
    #                         self.parent.db.scan_employee(qrcode_data)
    #                         print("[INFO] Found {} QR code: {}".format(qrcode_type, qrcode_data))
    #                     elif self.parent.db.check_temp(qrcode_data):
    #                         self.parent.db.scan_temp(qrcode_data)
    #                         print("[INFO] Found {} QR code: {}".format(qrcode_type, qrcode_data))
    #                     else:
    #                         wx.MessageBox('Сканованого QR-коду в базі данних немає!', 'Помилка!', wx.OK | wx.ICON_ERROR)
    #             if not self.text:
    #                 raise ValueError
    #     except ValueError:
    #         self.scan()
    #     finally:
    #         self.cam.release()
    #         cv2.destroyAllWindows()
