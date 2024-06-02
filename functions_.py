import time
import random
import pyautogui
import logging
import sys

logging.basicConfig(
    filename='error_log.log',  # Имя файла для записи логов
    level=logging.ERROR,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи логов
)


def rand_coord(start, finish):
    x = random.randint(start['X'], finish['X'])
    y = random.randint(start['Y'], finish['Y'])
    return {'x': x, 'y': y}


def write(text):
    pyautogui.write(text)


def press(button):
    pyautogui.press(button)


def click(X, Y):
    pyautogui.click(X, Y)


def doubleClick(X, Y):
    pyautogui.doubleClick(X, Y)


# press LMB to X&Y cords
def mouseDown(X, Y, button):
    pyautogui.mouseDown(x=X, y=Y, button=button)


# mouseUp
def mouseUp(button):
    pyautogui.mouseUp(button=button)


def moveTo(X, Y):
    pyautogui.moveTo(x=X, y=Y)


# pause with time_in_sec seconds
def pause(time_in_sec):
    time.sleep(time_in_sec)


def make_area_taps(X1, Y1, X2, Y2, duration, taps_per_sec):
    start = {'X': X1, 'Y': Y1}
    finish = {'X': X2, 'Y': Y2}

    total_taps = duration * taps_per_sec

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for _ in range(total_taps):
        cord = rand_coord(start, finish)
        click(cord['x'], cord['y'])
        pause(1 / (taps_per_sec + 1))
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


