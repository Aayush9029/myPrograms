import requests
from random import choice

def tellJokes():
    url = "https://raw.githubusercontent.com/EugeneKay/git-jokes/lulz/Jokes.txt"
    page = requests.get(url)

    jokes = page.text.split("\n")
    return choice(jokes)

