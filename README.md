# Keylogger

**DSCRIPTION:**

**Note that [L CTRL + F12] is the only way to stop the keylogger once it is running.**

This is a basic keylogger. It capturs keystorkes and records them locally in a file ```keylog.txt```.

The script will then email ```keylog.txt``` to a specified emaail address.

---

**FEATURES:**

- Local Storage: Stores logs in a file ```keylog.txt```.
- Email: Sends logs to a specified email address. Note: You must specicify the following:
    - Sender email address
    - Sender email address account password
    - To email address
    - SMTP server (default is ```smtp.gmail.com```)
    - Port number (default is 465)
- Program will run at startup after it is manually run once

---

**TROUBLESHOOTING:**

If your sender email address is a gmail ccount, and you are getting the following error:
```
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials k125-20020a37a183000000b005f170f7e497sm4061876qke.47 - gsmtp')
```
You may have to allow less secure apps to access your google account. 

More information here: https://support.google.com/accounts/answer/6010255

---


**DISCLAIMER:**

This keylogger was made for educational purposes only. I do not condone malicious useage of this keylogger.
