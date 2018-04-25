import numpy as np
from flask import jsonify

def numbers():
    mars_dict = {
    'news_title' : 1,
    'num1' : 1, 
    'num2' : 2,
    'num3' : 3,
    'num4' : 4,
    'num5' : 5}
    return mars_dict