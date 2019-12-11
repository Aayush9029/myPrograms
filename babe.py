#!/usr/local/bin/python3

# echo "\n add #!/usr/local/bin/python3 \n"
import pyautogui
import os
from sys import argv
import time


google_url = "https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
school_url = "https://byod.peelschools.org/"
school_login = ['XXXXXXXXXXXXX@pdsb.net']  # [1] == password but env will be used
youtube_url = "https://www.youtube.com/results?search_query="
google_url = "https://www.google.com/search?q="
spotify_url = "https://open.spotify.com/"
default_email = 'XXXXXXXXXXXXXXXXX'


def help():
    print('''
babe, version 0.25

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

    websites [url]
        example: ./babe website google.com
        example: ./babe ws writecode.me

    trello [name_of_project]
        example: ./babe trello automation
        example: ./babe trello app_weather

    spotify [song_name]
        example: ./babe spotify savant
        example: ./babe trello recent

    code [project name]
        example: ./babe code html
        example: ./babe code web_template
    ''')


def clear():
    pyautogui.hotkey('command', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('del')


def pressTab(number):
    for i in range(number):
        time.sleep(0.1)
        pyautogui.press('tab')


def openUrl(url):
    os.system('open -a firefox  --args -private-window ')
    time.sleep(1.5)
    pyautogui.hotkey('command', 't')
    pyautogui.typewrite(url)
    pyautogui.press('enter')
    time.sleep(5)


def vscode(projectName):
    print('Making a starter template in desktop named', projectName)
    where = "~/Desktop/" + projectName
    command = "mkdir " + where
    os.system(command)
    os.system("code "+where)
    time.sleep(3)
    pyautogui.hotkey('command', 'w')
    time.sleep(0.05)
    pyautogui.hotkey('command', 'n')
    pyautogui.typewrite('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
    <script src="main.js"></script>
</head>
<body>
</body>
</html>
    ''')
    time.sleep(0.3)
    pyautogui.hotkey('command', 's')
    time.sleep(1)
    pyautogui.typewrite('index.html')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('command', 'n')
    pyautogui.typewrite('''

    *{
    padding:0px;
    margin:0px;

    ''')
    time.sleep(0.3)

    pyautogui.hotkey('command', 's')
    time.sleep(1)

    pyautogui.typewrite("style.css")
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(0.5)

    pyautogui.hotkey('command', 'n')
    time.sleep(1)

    pyautogui.hotkey('command', 's')
    time.sleep(0.3)

    pyautogui.typewrite("main.js")
    time.sleep(0.3)

    pyautogui.press('enter')


def trello(projectName='Default'):
    os.system('open -a trello')
    time.sleep(2)
    pressTab(1)
    for i in range(4):
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
    pyautogui.typewrite('XXXXXXXXXXXXXX@gmail.com')
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

elif argv[1] == 'ws' or argv[1] == 'website' or argv[1] == 'site':
    openUrl(argv[2])

elif argv[1] == 'spotify' or argv[1] == 'spot':
    spotify(argv[2])

elif argv[1] == 'trello':
    trello(argv[2])

elif argv[1] == 'firefox':
    openUrl('')

elif argv[1] == 'code':
    vscode(argv[2])

elif argv[1] == 'clean':
    print("need root acces!")
    os.system("sudo -v")
    print(f"cleaning files..{os.getcwd()}")
    os.system("bash " + os.getcwd()+"/bin/clean.sh")


elif argv[1] == '-h' or argv[1] == '--help':
    help()

else:
    exit('no args? type \'--help or -h\' for help')
