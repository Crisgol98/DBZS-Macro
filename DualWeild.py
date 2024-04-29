from pynput.mouse import Button, Controller as MouseController
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Controller as KeyboardController
import threading
import time
import win32gui

mouse = MouseController()
keyboard = KeyboardController()
# Constantes
click_delay = 0.04
macro_active = False
senzu_active = False


def on_click(x, y, button, pressed):
    global macro_active
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Minecraft 1.7.10":
        return
    # Dual Weild
    if button == Button.x2 and pressed:
        macro_active = not macro_active
        if macro_active:
            threading.Thread(target=dual_weild).start()
    # Eat Senzu
    elif button == Button.x1 and pressed:
        macro_changed = False
        if macro_active:
            macro_active = False
            macro_changed = True
        if not senzu_active:
            threading.Thread(target=eat_senzu).start()
        if macro_changed:
            macro_active = True


def dual_weild():
    global macro_active
    while macro_active:
        mouse.click(Button.left)
        time.sleep(click_delay)
        keyboard.press('1')
        keyboard.release('1')
        time.sleep(click_delay)
        mouse.click(Button.left)
        time.sleep(click_delay)
        keyboard.press('2')
        keyboard.release('2')
        time.sleep(click_delay)


def eat_senzu():
    global macro_active, senzu_active
    senzu_active = True
    keyboard.press('9')
    keyboard.release('9')
    time.sleep(click_delay)
    mouse.click(Button.right)
    senzu_active = False


with MouseListener(on_click=on_click) as listener:
    listener.join()
