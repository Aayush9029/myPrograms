from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import json

font_file = '/Users/aayushpokharel/Library/Fonts/911Fonts.com_FuturaBoldItalic__-_911fonts.com_fonts_dgS7.ttf'

counter = 1

def makeQuote(qt, name):
    global counter
    www = len(qt.split())
    print("len of the quote is: ", www/2)
    para = textwrap.wrap(qt, width=www)
    im = Image.new("RGB", (1920, 1080))
    MAX_W, MAX_H = im.width, im.height
    quoteW = 0
    quoteH = 0
    fontSize = int(1000/www)

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font_file, fontSize)

    current_h, pad = MAX_H/4, 10

    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad
    
    wn, hn = draw.textsize(name, font=font)
    draw.text((MAX_W - 800, MAX_H - 400), "-"+name, font=font)
    
    im.save(f"image_quote{counter}.png")
    counter += 1





with open('quotes.json') as json_file:
    data = json.load(json_file)
    for d in data:
        name = d["name"]
        quote = d["quote"]
        makeQuote(quote,name)
        if counter > 2:
            exit()



