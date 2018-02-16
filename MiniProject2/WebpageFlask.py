from flask import Flask
from HW1API import get_tweets2vid
from HW1API import googlelabels
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
        for file in os.listdir():
            if file.endswith('.jpg'):
                os.remove(file)
        get_tweets2vid(screen_name='@Osama_amasO', number_tweets=5, rate=2)
        output = googlelabels(description_count=2)
        with open('labels.json') as handle:
            dictdump = json.loads(handle.read())
        return str(dictdump)

if __name__ == "__main__":
    app.run(debug=True)
