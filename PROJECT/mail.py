import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from consts import *

context = ssl.create_default_context()


async def send_mail(mail, path, subject='QR-код работника'):
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECIEVER
    msg['Subject'] = subject

    file = os.getcwd() + path + '/qr.png'
    with open(file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={file}')
    msg.attach(part)
    text = msg.as_string()

    with smtplib.SMTP_SSL(SMT_SERVER, PORT, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECIEVER, text)
