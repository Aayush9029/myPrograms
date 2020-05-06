from flask import Flask, request, render_template
import json

class Quote:
    '''
    To create a new quote and save do 
    
    >>> Quote("author", "quote")
    >>> Quote("Buddha", "Star the repo or something, have fun coding")

    '''
    def __init__(self, name, quote):
        self.name = name
        self.quote = quote


        with open("data/quotes.json", "a", encoding='utf-8') as quotes_file:
            data = {
                    "name": self.name,
                    "quote": self.quote
                    }
            json.dump(data, quotes_file, separators=(',', ':'))
            quotes_file.write(",\n")


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # print(request.form)
        name = request.form["username"]
        quote = request.form["quotes"]
        print("name: ", name)
        print("quote:", quote)
        Quote(name, quote)
    return render_template('index.html', error=error)



app.run(host='0.0.0.0', port=5555)
