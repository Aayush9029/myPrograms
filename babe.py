#!/usr/local/bin/python3

import pyautogui
import os
from sys import argv
import time

google_url = "https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
school_url = "https://byod.peelschools.org/"
school_login = ['927409@pdsb.net']  # [1] == password but env will be used
youtube_url = "https://www.youtube.com/results?search_query="
google_url = "https://www.google.com/search?q="
spotify_url = "https://open.spotify.com/"
default_email = 'aayushpokharel36@gmail.com'


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
        time.sleep(0.25)
        pyautogui.press('tab')

    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.typewrite(what)
    time.sleep(1)

    pyautogui.press('enter')


def spotify(song):

    pyautogui.press('enter')
    openUrl(spotify_url)
    for i in range(3):
        time.sleep(0.25)
        pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.typewrite(default_email)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)

# login ends now music time :)
    if(song == 'recent'):
        for i in range(3):
            time.sleep(0.25)
            pyautogui.press('tab')
        pyautogui.press('enter')

    else:
        # for i in range(3):
            # time.sleep(0.25)
        pyautogui.hotkey('command', 't')
        pyautogui.typewrite('https://open.spotify.com/search/' + song)
        pyautogui.press('enter')


def youtube(query):
    openUrl(youtube_url + query)


def google(query):
    openUrl(google_url + query)

# print(argv)


if(len(argv) == 1):
    exit('no args? type \'-help or h\' for help')

if(argv[1] == 'peel'):
    if len(argv) > 3:
        peelSchool(argv[2]+" "+argv[3])
    elif len(argv) > 1:
        peelSchool(argv[2])
    else:
        peelSchool('')

elif argv[1] == '--youtube' or argv[1] == '-yt' or argv[1] == 'youtube' or argv[1] == 'yt':
    youtube(argv[2])

elif argv[1] == '--google' or argv[1] == '-gg' or argv[1] == 'google' or argv[1] == 'gg':
    google(argv[2])

elif argv[1] == '--website' or argv[1] == '-site' or argv[1] == 'website' or argv[1] == 'site':
    openUrl(argv[2])

elif argv[1] == '--spotify' or argv[1] == '-spot' or argv[1] == 'spotify' or argv[1] == 'spot':
    spotify(argv[2])


elif argv[1] == '-h' or argv[1] == '--help':
    help()

else:
    exit('no args? type \'--help or -h\' for help')
