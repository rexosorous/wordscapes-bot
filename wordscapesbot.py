import pyautogui as mouse
from itertools import permutations

COL1 = 605
COL2 = 680
COL3 = 755

ROW1 = 425
ROW2 = 470
ROW3 = 560
ROW4 = 600


def move1():
    mouse.mouseDown(x=COL2, y=ROW1)

def move2():
    mouse.mouseDown(x=COL3, y=ROW2)

def move3():
    mouse.mouseDown(x=COL3, y=ROW3)

def move4():
    mouse.mouseDown(x=COL2, y=ROW4)

def move5():
    mouse.mouseDown(x=COL1, y=ROW3)

def move6():
    mouse.mouseDown(x=COL1, y=ROW2)


def move(pos: int):
    do = {1: move1,
        2: move2,
        3: move3,
        4: move4,
        5: move5,
        6: move6}

    do[pos]()


def bruteforce():
    threes = list(permutations(range(1,7), 3))
    fours = list(permutations(range(1,7), 4))
    fives = list(permutations(range(1,7), 5))
    sixes = list(permutations(range(1,7), 6))

    allcombos = threes + fours + fives + sixes

    for combo in allcombos:
        for pos in combo:
            move(pos)
        mouse.mouseUp()

bruteforce()