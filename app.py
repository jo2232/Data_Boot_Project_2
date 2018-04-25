from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import tweepy1
import google1

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/scrape')
def scrape():
    google = mongo.db.google
    data = google1.scrape_it()
    google.update(
        {},
        data,
        upsert=True
        )
    return redirect("http://127.0.0.1:5000/", code=302)

@app.route('/')
def index():
    google = mongo.db.google.find_one()
    return render_template('index.html', google=google)

@app.route('/twitterize')
def twitterize():
    data = tweepy1.twitterize()
    return jsonify(data)

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)
