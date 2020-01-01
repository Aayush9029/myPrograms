#!/usr/local/bin/python3

from pyautogui import press
from time import sleep
from os import system

print('auto press initiated..\nsetting brigtness to 0 soon')
sleep(10)
system("brightness 0")
sleep(1)


def moveKeys():
    # press('up') works well for spotify 
    press('tab')
    sleep(20)
    #press('down') spotify feature
    press('tab')
    sleep(20)
    moveKeys()


try:
    moveKeys()
except KeyboardInterrupt:
    exit("Bye")
