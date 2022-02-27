# Keylogger

**DISCLAIMER:**

This keylogger was made for educational purposes only. I do not condone malicious useage of this keylogger.

---

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
