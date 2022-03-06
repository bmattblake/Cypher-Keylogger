# Keylogger

**DESCRIPTION:**

**Note that [L CTRL + F12] is the only way to stop the keylogger once it is running.**

This is a basic keylogger. It captures keystrokes and records them locally in a file ```keylogs.txt```.

Immediately after the keylogger is stopped, the script will then email ```keylogs.txt``` to a specified email address.

---

**FEATURES:**

- Local Storage: Stores logs in a file ```keylogs.txt```.
- Email: Sends logs to a specified email address. Note: You must specify the following:
    - Sender email address
    - Sender email address account password
    - Recipient email address
    - SMTP server (default is ```smtp.gmail.com```)
    - Port number (default is 465)
- Program will automatically run at startup after it is manually executed once

---

**TROUBLESHOOTING:**

If your sender email address is a gmail account, and you are getting the following error:
```
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials k125-20020a37a183000000b005f170f7e497sm4061876qke.47 - gsmtp')
```
Make sure that you have entered the corrected login creditials.

If the problem persists, you may have to allow less secure apps to access your google account. 

- You can find more information on this subject here: https://support.google.com/accounts/answer/6010255.
- ***DO NOT DISABLE THIS FEATURE ON YOUR PERSONAL GMAIL ACCOUNT***. Disabling this security feature will make your google account more vulnerable to attacks. Making an entirely new google account hat is not associated with your personal account(s) is recommended.

If you get the following error:
```
ssl.SSLError: [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1129)
```
You have two options:
 - Make sure that your port number is 465. Port 465 is used for implicit TLS.
 - If you do not wish to use port 465, change line 109 from  
    ```server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)```  
    to  
    ```server = smtplib.SMTP(SMTP_SERVER, PORT)```

---


**DISCLAIMER:**

This keylogger was made for educational purposes only. I do not condone any use of this keylogger for malicious intent.
