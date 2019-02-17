import pyautogui
from itertools import permutations
from pynput.keyboard import Key, Listener
import threading
import os
import json
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'


# middle
COL1 = 175
COL2 = 285
COL3 = 390

ROW1 = 590
ROW2 = 650
ROW3 = 780
ROW4 = 840


# image sizes
WIDTH = 80
HEIGHT = 80


def move1():
    pyautogui.mouseDown(x=COL2, y=ROW1)

def move2():
    pyautogui.mouseDown(x=COL3, y=ROW2)

def move3():
    pyautogui.mouseDown(x=COL3, y=ROW3)

def move4():
    pyautogui.mouseDown(x=COL2, y=ROW4)

def move5():
    pyautogui.mouseDown(x=COL1, y=ROW3)

def move6():
    pyautogui.mouseDown(x=COL1, y=ROW2)


def move(pos: int):
    do = {1: move1,
        2: move2,
        3: move3,
        4: move4,
        5: move5,
        6: move6}

    do[pos]()







# load a dictionary so i don't have to brute force every combo, just ones that happen to be words
with open('words_dictionary.json') as file:
    dictionary = [word for word in list(json.load(file).keys()) if len(word) > 2 and len(word) < 7]




def start_level():
    pos1 = pyautogui.screenshot('images/pos1.png', region=(COL2 - int(WIDTH / 2), ROW1 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos2 = pyautogui.screenshot('images/pos2.png', region=(COL3 - int(WIDTH / 2), ROW2 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos3 = pyautogui.screenshot('images/pos3.png', region=(COL3 - int(WIDTH / 2), ROW3 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos4 = pyautogui.screenshot('images/pos4.png', region=(COL2 - int(WIDTH / 2), ROW4 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos5 = pyautogui.screenshot('images/pos5.png', region=(COL1 - int(WIDTH / 2), ROW3 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos6 = pyautogui.screenshot('images/pos6.png', region=(COL1 - int(WIDTH / 2), ROW2 - int(HEIGHT / 2), WIDTH, HEIGHT))


    print(pytesseract.image_to_string(pos1, config='--psm 10'))
    print(pytesseract.image_to_string(pos2, config='--psm 10'))
    print(pytesseract.image_to_string(pos3, config='--psm 10'))
    print(pytesseract.image_to_string(pos4, config='--psm 10'))
    print(pytesseract.image_to_string(pos5, config='--psm 10'))
    print(pytesseract.image_to_string(pos6, config='--psm 10'))


def bruteforce():
    threes = list(permutations(range(1,7), 3))
    fours = list(permutations(range(1,7), 4))
    fives = list(permutations(range(1,7), 5))
    sixes = list(permutations(range(1,7), 6))

    allcombos = [word for word in [threes + fours + fives + sixes] if word in dictionary]
    for combo in allcombos:
        for pos in combo:
            move(pos)
        pyautogui.mouseUp()





start_level()

# def stop(key):
#     if key == Key.esc:
#         print('stopped')
#         os._exit(1)


# def listen():
#     with Listener(on_press=stop) as listener:
#         listener.join()


# listen_therad = threading.Thread(target=listen)
# listen_thread.daemon = True
# listen_thread.start()

# bruteforce()