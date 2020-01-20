#!/usr/local/bin/python3

import pyautogui
import os
from sys import argv
import time
from random import randint


google_url = "https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
school_url = "https://byod.peelschools.org/"
school_login = [os.getenv("pdsb_EMAIL")]  # array is unnesessary but ehh
youtube_url = "https://www.youtube.com/results?search_query="
google_url = "https://www.google.com/search?q="
spotify_url = "https://open.spotify.com/"
default_email = os.getenv("a36_EMAIL").split("@")[0]
ifttApi = os.getenv("iftt_API_KEY")


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
    
    shutdown [minutes]
        example: ./babe shutdown 3
        example: ./babe shutdown 152


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


def clean():
    if randint(0, 10) < 1:   # restarts touch bar rarely
        print("killing touch bar..")
        os.system("pkill \"Touch Bar agent\"; killall \"ControlStrip\";")
        print("reviving.. touch bar")
    print("need root acces!")
    os.system("sudo -v")
    print("Cleaning firefox history...")
    os.system("sudo open -a firefox")
    time.sleep(1.5)
    pyautogui.hotkey("shift", "command", "delete")
    time.sleep(0.3)
    pyautogui.press("enter")
    pyautogui.hotkey("command", "q")
    time.sleep(0.5)
    print("Hold on tight cleaning safari history..")
    os.system("open -a safari")
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "optionleft", "enter")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "option", "h")
    time.sleep(0.4)
    pyautogui.mouseDown(856, 185)
    pyautogui.mouseUp()
    time.sleep(0.2)
    print("Emptying safari chaches")
    pyautogui.hotkey("option", "command", "e")
    time.sleep(0.3)
    print("Safari cleaning complete")
    pyautogui.hotkey("command", "q")
    print(f"Cleaning files..{os.getcwd()}")
    os.system("bash " + os.getcwd()+"/bin/clean.sh")
    os.system("cd;rm -rf .zsh_history")
    if len(os.listdir(f"{os.getcwd()}/Downloads")) > 0:
        print("\n\n")
        for i in os.listdir(f"{os.getcwd()}/Downloads"):
            print(f"--> {i}")
        ask = input(
            "Here are all the files and folders in downloads directory,\nwould you like to permanently delete them?: ")
        if ask.lower() == 'y':
            print("removing all files from downloads...")
            os.system("rm -rf ~/Downloads")
            print("done...")
            os.system(f"mkdir {os.getcwd()}/Downloads")
            exit("cleaning complete...")

        else:
            exit("cleaning complete...")


def peelSchool(what):
    openUrl(school_url)
    clear()
    pyautogui.typewrite(school_login[0])
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')
    pressTab(9)
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
    pyautogui.typewrite(os.getenv("a36_EMAIL"))
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
    try:
        clean()
    except KeyboardInterrupt:
        exit("Process stopped.")

elif argv[1] == 'shutdown' or argv[1] == 'shut':
    i = input("after how many minutes? ")
    print(i, "minutes starting now...")
    os.system(f"sudo shutdown -h +{i}")

elif argv[1] == '-h' or argv[1] == '--help':
    help()

else:
    exit('no args? type \'--help or -h\' for help')
