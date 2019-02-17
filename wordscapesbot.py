import pyautogui
from itertools import permutations
from pynput.keyboard import Key, Listener
from collections import Counter
import threading
import os
import json
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'


# middle
COL1 = 175
COL2 = 285
COL3 = 390

ROW1 = 585
ROW2 = 645
ROW3 = 775
ROW4 = 835


# image sizes
WIDTH = 70
HEIGHT = 70


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
    dictionary = [word.upper() for word in list(json.load(file).keys()) if len(word) > 2 and len(word) < 7]




def start_level():
    pos1 = pyautogui.screenshot('images/pos1.png', region=(COL2 - int(WIDTH / 2), ROW1 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos2 = pyautogui.screenshot('images/pos2.png', region=(COL3 - int(WIDTH / 2), ROW2 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos3 = pyautogui.screenshot('images/pos3.png', region=(COL3 - int(WIDTH / 2), ROW3 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos4 = pyautogui.screenshot('images/pos4.png', region=(COL2 - int(WIDTH / 2), ROW4 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos5 = pyautogui.screenshot('images/pos5.png', region=(COL1 - int(WIDTH / 2), ROW3 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pos6 = pyautogui.screenshot('images/pos6.png', region=(COL1 - int(WIDTH / 2), ROW2 - int(HEIGHT / 2), WIDTH, HEIGHT))


    char_pos = [[pytesseract.image_to_string(pos1, config='--psm 10'), 1],
    [pytesseract.image_to_string(pos2, config='--psm 10'), 2],
    [pytesseract.image_to_string(pos3, config='--psm 10'), 3],
    [pytesseract.image_to_string(pos4, config='--psm 10'), 4],
    [pytesseract.image_to_string(pos5, config='--psm 10'), 5],
    [pytesseract.image_to_string(pos6, config='--psm 10'), 6]]

    for x in char_pos:
        if x[0] == '|':
            x[0] = 'I'

    bruteforce(char_pos)



def bruteforce(char_pos: dict):
    threes = list(map(''.join, permutations([char[0] for char in char_pos], 3)))
    fours = list(map(''.join, permutations([char[0] for char in char_pos], 4)))
    fives = list(map(''.join, permutations([char[0] for char in char_pos], 5)))
    sixes = list(map(''.join, permutations([char[0] for char in char_pos], 6)))

    allcombos = [word for word in threes + fours + fives + sixes if word in dictionary]


    for combo in allcombos:
        dupes = [k for k,v in Counter(combo).items() if v>1]
        dupe_dict = {}
        for char in dupes:
            dupe_dict[char] = [r[1] for r in char_pos if r[0] == char]

        for char in combo:
            if char in dupes:
                move(dupe_dict[char][0])
                del(dupe_dict[char][0])
            else:
                for ele in char_pos:
                    if ele[0] == char:
                        move(ele[1])
        pyautogui.mouseUp()




def stop(key):
    if key == Key.esc:
        print('stopped')
        os._exit(1)


def listen():
    with Listener(on_press=stop) as listener:
        listener.join()


listen_thread = threading.Thread(target=listen)
listen_thread.daemon = True
listen_thread.start()




start_level()