#!/usr/local/bin/python3

import pyautogui
import os
from sys import argv
import time


google_url = "https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
school_url = "https://xx.xxxxxx.org/"
school_login = ['xxxxx@xxxxx.net']  # [1] == password env 
youtube_url = "https://www.youtube.com/results?search_query="
google_url = "https://www.google.com/search?q="
spotify_url = "https://open.spotify.com/"
default_email = 'xxxxxx' 
ifttApi = "xxxxxxxxxxxxxxx/" 


def help():
    print('''
babe, version 0.2

usage: babe [keyword] [name/query]

    peel [query]
        example: ./babe peel google docs
        example: ./babe peel classroom

    youtube [query]  login
        example: ./babe youtube cats
        example: ./babe yt login <--logs into yt account

    google [query]
        example: ./babe google duckduckgo
        example: ./babe gg login <--logs into google account

    trello [name_of_project]
        example: ./babe trello automation
        example: ./babe trello app_weather

    spotify [song_name]
        example: ./babe spotify savant
        example: ./babe trello recent

    code [project name]
        example: ./babe code html
        example: ./babe code web_template

    clean 
        example: ./babe clean <-- purges cache, logs.. 

    ping [device]
        example: ./babe ping iPhone 
        example: ./babe ping phone 

    lamp [state]
        example: ./babe lamp on 
        example: ./babe lamp off 

    tv [state]
        example: ./babe tv on 
        example: ./babe tv off 


    ''')


def clear():
    pyautogui.hotkey('command', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('del')


def pressTab(number):
    for _ in range(number):
        time.sleep(0.1)
        pyautogui.press('tab')


def openUrl(url):
    os.system('open -a firefox  --args -private-window ')
    time.sleep(1.5)
    pyautogui.hotkey('command', 't')
    pyautogui.typewrite(url)
    pyautogui.press('enter')
    time.sleep(5)


def vscode(name):
    location = f"~/Desktop/{name}"
    print("started setting up project in", location)
    print("making copy of html_template.")
    os.system(f"cp -a bin/html_template {location}")
    print("opening project in vscode")
    os.system(f"code {location}")


def trello(projectName='Default'):
    os.system('open -a trello')
    time.sleep(2)
    pressTab(1)
    for _ in range(4):
        pyautogui.hotkey('shift', 'tab')
    pyautogui.press('enter')
    pressTab(2)
    pyautogui.press('enter')
    pyautogui.typewrite(projectName)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite('Need to do')
    pyautogui.press('enter')
    pyautogui.typewrite('Doing')
    pyautogui.press('enter')
    pyautogui.typewrite('Done')
    pyautogui.press('enter')
    pyautogui.typewrite('Might do')
    pyautogui.press('enter')


def lamp(state):
    if state == 'on':
        state = 'lampOn'
    else:
        state = 'lampOff'

    os.system("curl -X POST https://maker.ifttt.com/trigger/\{" +
              state
              + "}/with/key/" + ifttApi)


def tv(state):
    if state == 'on':
        state = 'tvOn'
    else:
        state = 'tvOff'

    os.system("curl -X POST https://maker.ifttt.com/trigger/\{" +
              state
              + "}/with/key/" + ifttApi)


def ping(device):
    if device == 'iPhone' or device == 'phone':
        device = "ping_myiPhone"

    os.system(
        "curl -X POST https://maker.ifttt.com/trigger/\{"+device+"}/with/key/"+ifttApi)


def googleDefault():
    openUrl('https://www.google.com')
    pressTab(8)
    pyautogui.press('enter')


def youtubeDefault():
    openUrl('https://www.youtube.com')
    time.sleep(2)
    pressTab(8)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite(default_email)
    pyautogui.press('enter')
    time.sleep(2)
    clear()
    pyautogui.press('down')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.press('enter')

    # pyautogui.press('enter')


def peelSchool(what):
    openUrl(school_url)
    clear()
    pyautogui.typewrite(school_login[0])
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')
    pressTab(8)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite(what)
    time.sleep(1)
    pyautogui.press('enter')


def spotify(song):
    pyautogui.press('enter')
    openUrl(spotify_url)
    pressTab(4)
    pyautogui.press('enter')
    time.sleep(4)
    clear()
    pyautogui.typewrite('xxxxxxxxxxxxx@gmail.com')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)


# login ends now music time :)
    if(song == 'recent'):
        pressTab(4)
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


if(len(argv) == 1):
    exit('no args? type \'-help or h\' for help')

if(argv[1] == 'peel'):
    if len(argv) > 3:
        peelSchool(argv[2]+" "+argv[3])
    elif len(argv) > 1:
        peelSchool(argv[2])
    else:
        peelSchool('')

elif argv[1] == 'youtube' or argv[1] == 'yt':
    if(argv[2] == 'login'):
        youtubeDefault()
    else:
        youtube(argv[2])

elif argv[1] == 'google' or argv[1] == 'gg':
    if(argv[2] == 'login'):
        googleDefault()
    else:
        google(argv[2])


elif argv[1] == 'spotify' or argv[1] == 'spot':
    spotify(argv[2])

elif argv[1] == 'trello':
    trello(argv[2])

elif argv[1] == 'firefox':
    openUrl('')

elif argv[1] == 'code':
    vscode(argv[2])

elif argv[1] == 'lamp':
    lamp(argv[2])
elif argv[1] == 'ping':
    ping(argv[2])

elif argv[1] == 'tv':
    tv(argv[2])

elif argv[1] == 'clean':
    print("need root acces!")
    os.system("sudo -v")
    os.system("sudo open -a firefox")
    print(f"cleaning files..{os.getcwd()}")
    os.system("bash " + os.getcwd()+"/bin/clean.sh")

elif argv[1] == '-h' or argv[1] == '--help':
    help()

else:
    exit('no args? type \'--help or -h\' for help')
