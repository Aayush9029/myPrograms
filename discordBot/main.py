import discord
import os 
import random 

from weather.app import showWeather
from modules.randomNumber import generaterandom
from modules.jokes import tellJokes

token = os.getenv('dis')





def checkMessages(msg):
    msg = msg.lower()
    if "cat" in msg:
        return "Kitten i love kitten"


    if "lamp on" in msg:
        return "turning lamp on"

    if "weather" in msg:
        if "in" in msg:
            m = msg.split()
            i = m.index("in")
            return showWeather(m[i+1])
        else:
            return showWeather("mississauga")

    if "number" and "pick" in msg:
        return str(generaterandom(msg))

    if "joke" in msg:
        return tellJokes()












class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        
        new = checkMessages(message.content)

        
        if new != None:
            await message.channel.send(new)
































client = MyClient()
client.run(token)
exit("Bye")
