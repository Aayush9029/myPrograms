#!/usr/local/bin/python3

import pyautogui
import os
from sys import argv
import time

google_url = "https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
school_url = "https://byod.peelschools.org/"
school_login = ['your@email.com']  # [1] == password but env will be used


def help():
    print('''
babe, version 0.1

usage: babe [peel] [-yt --youtube] [-gg --google] [-site --website]

    peel [query] 
        example: ./babe peel google docs
        example: ./babe peel classroom 

    youtube [query]
        example: ./babe youtube cats 
        example: ./babe yt pwediepie 

    google [query]
        example: ./babe google duckduckgo 
        example: ./babe gg memes 

    websites [url]
        example: ./babe website google.com 
        example: ./babe ws writecode.me 

    ''')


def clear():
    pyautogui.hotkey('command', 'a')
    pyautogui.hotkey('del')


def openUrl(url):
    os.system('open -a firefox  --args -private-window ' + url)
    time.sleep(5)


def peelSchool(what):
    openUrl(school_url)
    clear()
    pyautogui.typewrite(school_login[0])
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')

    for i in range(8):
        pyautogui.press('tab')

    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.typewrite(what)
    time.sleep(1)

    pyautogui.press('enter')


# print(argv)

if(len(argv) == 1):
    exit('no args? type \'-help or h\' for help')

if(argv[1] == 'peel'):
    if len(argv) > 2:
        peelSchool(argv[2]+" "+argv[3])
    elif len(argv) > 1:
        peelSchool(argv[2])
    else:
        peelSchool('')

elif argv[1] == '--youtube' or argv[1] == '-yt' or argv[1] == 'youtube' or argv[1] == 'yt':
    exit('yt in progress')

elif argv[1] == '--google' or argv[1] == '-gg' or argv[1] == 'google' or argv[1] == 'gg':
    exit('google in progress')

elif argv[1] == '--website' or argv[1] == '-site' or argv[1] == 'website' or argv[1] == 'site':
    exit('web in progress')

elif argv[1] == '-h' or argv[1] == '--help':
    help()

else:
    exit('no args? type \'--help or -h\' for help')
