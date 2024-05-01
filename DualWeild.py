from pynput.mouse import Button, Controller as MouseController
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Controller as KeyboardController
import threading
import time
import win32gui
import signal

mouse = MouseController()
keyboard = KeyboardController()
# Constantes
click_delay = 0.04
senzu_delay = 0.01
macro_active = False
senzu_active = False
senzu_clicked = 0
senzu_worked = 0


# Define una clase para manejar la señal de interrupción
class InterruptionHandler:
    def __init__(self):
        self.interrupted = False
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        self.interrupted = True


# Crea una instancia del manejador de interrupción
interruption_handler = InterruptionHandler()


def on_click(x, y, button, pressed):
    global macro_active, senzu_active, senzu_clicked
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Minecraft 1.7.10":
        return
    if button == Button.x2 and pressed:
        macro_active = not macro_active
        if macro_active:
            threading.Thread(target=dual_weild).start()
    elif button == Button.x1 and pressed:
        if senzu_active:
            return
        senzu_active = True
        senzu_clicked += 1
        print(f'senzu button clicked {senzu_clicked} times and worked {senzu_worked+1} times')
        threading.Thread(target=eat_senzu).start()


def dual_weild():
    global macro_active
    while macro_active and not interruption_handler.interrupted:
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
    global senzu_active, senzu_worked
    keyboard.press('9')
    keyboard.release('9')
    time.sleep(senzu_delay)
    mouse.click(Button.right)
    time.sleep(senzu_delay)
    mouse.click(Button.right)
    time.sleep(senzu_delay)
    senzu_worked += 1
    senzu_active = False


with MouseListener(on_click=on_click) as listener:
    listener.join()
