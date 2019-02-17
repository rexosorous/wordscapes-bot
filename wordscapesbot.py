import pyautogui
from time import sleep
from itertools import permutations
from pynput.keyboard import Key, Listener
from collections import Counter
import threading
import os
import json
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'



class OCR_Error(Exception):
    pass



# middle
COL1 = 176
COL2 = 284
COL3 = 393

ROW1 = 584
ROW2 = 647
ROW3 = 772
ROW4 = 836


# image sizes
WIDTH = 70
HEIGHT = 66


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

def click_shuffle():
    pyautogui.click(53, 514)

def click_level():
    pyautogui.click(250, 725)

def click_world():
    pyautogui.click(295, 290)


def check_red() -> int:
    return pyautogui.pixel(80, 867)[0]


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





def screenshot():
    pyautogui.screenshot('images/pos1.png', region=(COL2 - int(WIDTH / 2), ROW1 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pyautogui.screenshot('images/pos2.png', region=(COL3 - int(WIDTH / 2), ROW2 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pyautogui.screenshot('images/pos3.png', region=(COL3 - int(WIDTH / 2), ROW3 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pyautogui.screenshot('images/pos4.png', region=(COL2 - int(WIDTH / 2), ROW4 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pyautogui.screenshot('images/pos5.png', region=(COL1 - int(WIDTH / 2), ROW3 - int(HEIGHT / 2), WIDTH, HEIGHT))
    pyautogui.screenshot('images/pos6.png', region=(COL1 - int(WIDTH / 2), ROW2 - int(HEIGHT / 2), WIDTH, HEIGHT))

    pos1 = cv2.cvtColor(cv2.imread('images/pos1.png'), cv2.COLOR_BGR2GRAY)
    pos2 = cv2.cvtColor(cv2.imread('images/pos2.png'), cv2.COLOR_BGR2GRAY)
    pos3 = cv2.cvtColor(cv2.imread('images/pos3.png'), cv2.COLOR_BGR2GRAY)
    pos4 = cv2.cvtColor(cv2.imread('images/pos4.png'), cv2.COLOR_BGR2GRAY)
    pos5 = cv2.cvtColor(cv2.imread('images/pos5.png'), cv2.COLOR_BGR2GRAY)
    pos6 = cv2.cvtColor(cv2.imread('images/pos6.png'), cv2.COLOR_BGR2GRAY)

    pos1 = cv2.threshold(pos1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    pos2 = cv2.threshold(pos2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    pos3 = cv2.threshold(pos3, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    pos4 = cv2.threshold(pos4, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    pos5 = cv2.threshold(pos5, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    pos6 = cv2.threshold(pos6, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    pos1 = cv2.medianBlur(pos1, 3)
    pos2 = cv2.medianBlur(pos2, 3)
    pos3 = cv2.medianBlur(pos3, 3)
    pos4 = cv2.medianBlur(pos4, 3)
    pos5 = cv2.medianBlur(pos5, 3)
    pos6 = cv2.medianBlur(pos6, 3)

    cv2.imwrite('images/pos1.png', pos1)
    cv2.imwrite('images/pos2.png', pos2)
    cv2.imwrite('images/pos3.png', pos3)
    cv2.imwrite('images/pos4.png', pos4)
    cv2.imwrite('images/pos5.png', pos5)
    cv2.imwrite('images/pos6.png', pos6)



def start_level():
    while True:
        sentinel = True
        screenshot()

        char_pos = [[pytesseract.image_to_string('images/pos1.png', config='--psm 10'), 1],
            [pytesseract.image_to_string('images/pos2.png', config='--psm 10'), 2],
            [pytesseract.image_to_string('images/pos3.png', config='--psm 10'), 3],
            [pytesseract.image_to_string('images/pos4.png', config='--psm 10'), 4],
            [pytesseract.image_to_string('images/pos5.png', config='--psm 10'), 5],
            [pytesseract.image_to_string('images/pos6.png', config='--psm 10'), 6]]

        for x in char_pos:
            x[0] = x[0].upper()
            if x[0] == '|':
                x[0] = 'I'
            if len(x[0]) != 1:
                sentinel = False
        print([x[0] for x in char_pos])

        if sentinel:
            break
        click_shuffle()
        sleep(1.5)

    bruteforce(char_pos)



def bruteforce(char_pos: dict):
    threes = list(map(''.join, permutations([char[0] for char in char_pos], 3)))
    fours = list(map(''.join, permutations([char[0] for char in char_pos], 4)))
    fives = list(map(''.join, permutations([char[0] for char in char_pos], 5)))
    sixes = list(map(''.join, permutations([char[0] for char in char_pos], 6)))

    if check_red() > 245 and check_red() < 258:
        allcombos = set([word for word in fours + fives + sixes if word in dictionary])
    else:
        allcombos = set([word for word in threes + fours + fives + sixes if word in dictionary])

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
                        break
        pyautogui.mouseUp()



def next_level():
    sleep(12)

    pyautogui.screenshot('images/next_level.png', region=(200, 719, 180, 40))
    # level_img = cv2.cvtColor(cv2.imread('images/next_level.png'), cv2.COLOR_BGR2GRAY)
    # level_img = cv2.threshold(level_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv2.imwrite('images/next_level.png', level_img)
    level_text = pytesseract.image_to_string('images/next_level.png').upper()
    print(level_text)
    if 'LEVEL' in level_text:
        print (level_text)
        click_level()
        sleep(1)
    elif 'COLLECT' in level_text:
        print('world end')
        pyautogui.press('esc')
        sleep(3)
        pyautogui.press('esc')
        sleep(1)
        click_world()
        sleep(1)
    else:
        click_shuffle()






def stop(key):
    if key == Key.space:
        print('manual stop')
        os._exit(1)


def listen():
    with Listener(on_press=stop) as listener:
        listener.join()


listen_thread = threading.Thread(target=listen)
listen_thread.daemon = True
listen_thread.start()



while True:
    start_level()
    next_level()