#!/usr/local/bin/python3

from pyautogui import press
from time import sleep
from os import system

print('auto press initiated..\nsetting brigtness to 0 soon')
sleep(10)
system("brightness 0")
sleep(1)


def moveKeys():
    # print('up')
    press('up')
    sleep(20)
    # print('up')
    press('down')
    sleep(20)
    moveKeys()


try:
    moveKeys()
except KeyboardInterrupt:
    exit("Bye")
