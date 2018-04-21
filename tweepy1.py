import numpy as np
from flask import jsonify

def numbers():

    mars_dict = {
    'news_title' : 'THIS IS FROM TWEEPY MONGO DB HI MOM',
    'news_summary' : 'hi', 
    'featured_image_url' : 'hi',
    'mars_weather' : 'hi',
    'table_string' : 'hi',
    'hemisphere_image_urls' : 'hi'}
    return mars_dict
