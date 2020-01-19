from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import json

array = []

counter = 1
with open('quotes.json') as json_file:
    data = json.load(json_file)
    for p in data['quotes']:
        # print(p['quote'])
        array.append(p['quote'])


def makeQuote(qt):
    global counter
    para = textwrap.wrap(qt, width=20)
    im = Image.open(f"images/{counter}.png")
    MAX_W, MAX_H = im.width, im.height

    fontSize = int(MAX_W/15)

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', fontSize)

    current_h, pad = MAX_H/4, 10

    for line in para:
        line = line.upper()
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad
    im.save(f"quotes/{counter}_quote.png")


for qt in array:
    makeQuote(qt)
    counter += 1
    if counter > 5:
        exit('done for now')
