# Dependencies
import json
import time
import os
import requests
import twitter      # pip install python-twitter or twitter-python?
import numpy as np
import random

# Setting up Vader
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Setting up Mongo
import pymongo
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.tweets_db

# Setting Keys
consumer_key = 'SZuyqX69qC9kH9juCBquOuA45'
consumer_secret = 'sb93EajIYsEY0t1iA7Vpl9brgweYVxdiYjIhUPgeOgZdJuuBoq'
access_token = '955959610543833089-D7tNeGFMdMPtNVBBlJCZvOL2H1Kb4sp'
access_token_secret = 't6aGaAqbbY1C6nLAKDENl3NiqFu1RHjNtCmoXbBSFfkFN'

# Setting up Auth
api = twitter.Api(consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_key=access_token,
                access_token_secret=access_token_secret)


# Tweet Gather function
def tweetGrab(city, city_dict, start_time):

    # Call to API - each new call should return new tweets and count against rate-limit
    tweets = api.GetSearch(geocode=[city_dict[f'{city}']['gps'][1],city_dict[f'{city}']['gps'][0], '20mi'],return_json=True,count=100)

    # Loop to parse tweet and append data needed
    for tweet in tweets['statuses']:
        
        # Temp dict do pass into function instead of whole data file
        temp_dict = {
            'tempText': [],
            'tempBox': [],
            'tempUser': [],
            'tempCreated_at': [],
            'tempFollowers_count': [],
            'temp_id': [],
            'tempComp': [],
            'tempCords': [],
            'tempImg': []         
        }

        # If loop to ensure unique tweets
        if tweet['id'] in city_dict[f'{city}']['data']['id']:
            continue
        else:
            # Temp variables
            temp_dict['tempText'].append(tweet['text'])
            temp_dict['tempBox'].append(solveBox(tweet['place']['bounding_box']['coordinates']))
            temp_dict['tempUser'].append(tweet['user']['screen_name'])
            temp_dict['tempCreated_at'].append(tweet['created_at'])
            temp_dict['tempFollowers_count'].append(tweet['user']['followers_count'])
            temp_dict['temp_id'].append(tweet['id'])
            temp_dict['tempComp'].append(analyzer.polarity_scores(tweet['text'])['compound'])
           
            # Creating try loops for variable data that may or may not show up
            try:
                temp_dict['tempCords'].append(tweet['coordinates']['coordinates'])
            except:
                temp_dict['tempCords'].append(tweet['coordinates'])

            try:
                temp_dict['tempImg'].append(tweet['user']['profile_image_url'])
            except:
                temp_dict['tempImg'].append('None')
            
            # Sending things over to Mongo for storage
            updateMongo(temp_dict, city)
            
            # Appending important data from temp dict
            city_dict[f'{city}']['data']['text'].append(temp_dict['tempText'][0])
            city_dict[f'{city}']['data']['bounding_box'].append(temp_dict['tempBox'][0])
            city_dict[f'{city}']['data']['user'].append(temp_dict['tempUser'][0])
            city_dict[f'{city}']['data']['created_at'].append(temp_dict['tempCreated_at'][0])
            city_dict[f'{city}']['data']['followers_count'].append(temp_dict['tempFollowers_count'][0])
            city_dict[f'{city}']['data']['comp_sent'].append(temp_dict['tempComp'][0])
            city_dict[f'{city}']['data']['id'].append(temp_dict['temp_id'][0])
            city_dict[f'{city}']['data']['coords'].append(temp_dict['tempCords'][0])
            city_dict[f'{city}']['data']['profile_image_url'].append(temp_dict['tempImg'][0])


            # Printing status of calls and current time
            if (len(city_dict[f'{city}']['data']['id'])%5 == 0):
                print(f'{city}: ' + str(len(city_dict[f'{city}']['data']['id'])) + ' --- %s seconds' % round(time.clock() - start_time,2))    

    # Ending function
    return()


# Calculating a rough coord based on bounding box
def solveBox(bounding_box):
    
    # Creating temp dict and variable to return
    coord_dict = {'lat': [], 'lon': []}
    coord_return = []

    # Small loop to append each coord to it's own list to sum
    for coord in bounding_box[0]:
        coord_dict['lat'].append(coord[1] + random.uniform(-.005,.005))
        coord_dict['lon'].append(coord[0] + random.uniform(-.005,.005))

    # Appending the sums to a return list
    coord_return.append(round(np.mean(coord_dict['lon']),6))
    coord_return.append(round(np.mean(coord_dict['lat']),6))

    # Return list of coords
    return(coord_return)


# Fills out the dictionary
def fillDict():
    
    # City dictionary with static coords
    city_dict = {
        'Dallas': {'gps':[-96.796988, 32.776664], 'data':{}},
        'St. Louis': {'gps':[-90.199404, 38.627003], 'data':{}},
        'Los Angeles': {'gps':[-118.243685, 34.052234], 'data':{}},
        'Atlanta': {'gps':[-84.387982, 33.748995], 'data':{}},
        'Chicago': {'gps':[-87.629798, 41.878114], 'data':{}},
        'Miami': {'gps':[-80.191790, 25.761680], 'data':{}},
        'New York': {'gps':[-74.005973, 40.712775], 'data':{}},
        'Kansas City': {'gps':[-94.578567, 39.099727], 'data':{}},
        'Seattle': {'gps':[-122.332071, 47.606210], 'data':{}},
        'Las Vegas': {'gps':[-115.139830, 36.169941], 'data':{}}
        }

    # Adding template to dictionary
    for city in city_dict:

        # Making lists for each entry
        city_dict[f'{city}']['data']['text'] = [] 
        city_dict[f'{city}']['data']['coords'] = []
        city_dict[f'{city}']['data']['bounding_box'] = []
        city_dict[f'{city}']['data']['user'] = []
        city_dict[f'{city}']['data']['profile_image_url'] = []
        city_dict[f'{city}']['data']['created_at'] = []
        city_dict[f'{city}']['data']['comp_sent'] = []
        city_dict[f'{city}']['data']['followers_count'] = []
        city_dict[f'{city}']['data']['id'] = []

    # Returning the dictionary
    return(city_dict)


# Function to compress limit check
def limit_check(check, city_dict, tweet_goal):
    
    # Creating empty check list
    check_arr = []
    
    # Checking if any of the lists have reached the limit
    if (check == 'first_to_goal'):
        for city in city_dict:
            if (len(city_dict[f'{city}']['data']['text'])>=tweet_goal):
                check_arr.append(True)
            else:
                check_arr.append(False)
                
        # Setting limit based on 'not any' logic
        limit = not any(check_arr)
    
    # Checking if all the lists have reached the limit
    if (check == 'all_to_goal'):
        for city in city_dict:
            if (len(city_dict[f'{city}']['data']['text'])<tweet_goal):
                check_arr.append(True)
            else:
                check_arr.append(False)   
        
        # Setting limit based on 'any' logic
        limit = any(check_arr)
    
    # Returning a bool to check against for loop
    return(limit)


# Save output to a txt/json doc for easy read later
def saveOutput(data, tweet_goal, start_time, limit_type):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 2)
    with open(f'{limit_type} - {tweet_goal} Tweets - ' + str(round(time.clock()-start_time,2)) + f' Runtime - {start_time}.txt', 'w') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 2)


# Print Final Output
def printOutput(city_dict, start_time):
    
    # Starting printing format
    print('-------------------------------------------')
    
    # Loop to print each list length
    for city in city_dict:
        print(f'{city}:' + str(len(city_dict[f'{city}']['data']['text'])))
    
    # Final Format Print with runtime
    print('-------------------------------------------')
    print('--- %s Runtime' % round(time.clock() - start_time,2))

# Update to MongoDB
def updateMongo(temp_dict, city):
    db.city.insert_one({
        'bounding_box': temp_dict['tempBox'][0], 
        'cords': temp_dict['tempCords'][0], 
        'comp_sent': temp_dict['tempComp'][0], 
        'created_at': temp_dict['tempCreated_at'][0],
        'followers_count': temp_dict['tempFollowers_count'][0],
        'profile_image_url': temp_dict['tempImg'][0],
        'text': temp_dict['tempText'][0],
        'user': temp_dict['tempUser'][0],
        'tweet_id': temp_dict['temp_id'][0],
        'city': city
    })

# Main Execution
def twitterize():
    
    # Setting up statics
    tweet_goal = 100
    limit_type = 'first_to_goal' # 'first_to_goal' or 'all_to_goal'
    start_time = time.clock()
    
    # Finding the dict
    city_dict = fillDict()

    # Main loop - Checks what type of limit is set and runs until False is returned
    while (limit_check(limit_type, city_dict, tweet_goal) == True):
        
        # Rotates cities - Causes a delay so new tweets can be fed to the API
        for city in city_dict:
            tweetGrab(city, city_dict, start_time)
            time.sleep(6)

    # Saving output to txt file
    saveOutput(city_dict, tweet_goal, start_time, limit_type)
    
    # Printing runtime
    printOutput(city_dict, start_time)

    return(city_dict)