
# Dependencies
import json
import time
import os
import requests
import twitter
import numpy as np
from flask import Flask, jsonify, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Setting up Vader
analyzer = SentimentIntensityAnalyzer()

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
    tweets = api.GetSearch(geocode=[city_dict[f'{city}']['gps'][1],city_dict[f'{city}']['gps'][0], '20mi'],return_json=True)

    # Loop to parse tweet and append data needed
    for tweet in tweets['statuses']:

        # If loop to ensure unique tweets
        if tweet['text'] in city_dict[f'{city}']['data']['text']:
            continue
        else:        
            # Appending important data
            city_dict[f'{city}']['data']['text'].append(tweet['text'])
            city_dict[f'{city}']['data']['bounding_box'].append(solveBox(tweet['place']['bounding_box']['coordinates']))
            city_dict[f'{city}']['data']['user'].append(tweet['user']['screen_name'])
            city_dict[f'{city}']['data']['created_at'].append(tweet['created_at'])
            city_dict[f'{city}']['data']['followers_count'].append(tweet['user']['followers_count'])
            city_dict[f'{city}']['data']['comp_sent'].append(analyzer.polarity_scores(tweet['text'])['compound'])

            # Creating try loops for variable data that may or may not show up
            try:
                city_dict[f'{city}']['data']['coords'].append(tweet['coordinates']['coordinates'])
            except:
                city_dict[f'{city}']['data']['coords'].append(tweet['coordinates'])

            try:
                city_dict[f'{city}']['data']['profile_image_url'].append(tweet['user']['profile_image_url'])
            except:
                city_dict[f'{city}']['data']['profile_image_url'].append('None')

            # Printing status of calls and current time
            if (len(city_dict[f'{city}']['data']['text'])%5 == 0):
                print(f'{city}: ' + str(len(city_dict[f'{city}']['data']['text'])) + ' --- %s seconds' % round(time.clock() - start_time,2))    

    # Ending function
    return()


# In[5]:


# Calculating a rough coord based on bounding box
def solveBox(bounding_box):
    
    # Creating temp dict and variable to return
    coord_dict = {'lat': [], 'lon': []}
    coord_return = []

    # Small loop to append each coord to it's own list to sum
    for coord in bounding_box[0]:
        coord_dict['lat'].append(coord[1] + (np.random.rand() - np.random.rand()))
        coord_dict['lon'].append(coord[0] + (np.random.rand() - np.random.rand()))

    # Appending the sums to a return list
    coord_return.append(round(np.mean(coord_dict['lon']),6))
    coord_return.append(round(np.mean(coord_dict['lat']),6))

    # Return list of coords
    return(coord_return)


# In[6]:


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
        'Las Vegas': {'gps':[-115.139830, 36.169941], 'data':{}},


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

    # Returning the dictionary
    return(city_dict)


# In[7]:


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


# In[8]:


# Save output to a txt/json doc for easy read later
def saveOutput(data, tweet_goal, start_time, limit_type):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 2)
    with open(f'{limit_type} - {tweet_goal} Tweets - ' + str(round(time.clock()-start_time,2)) + f' Runtime - {start_time}.txt', 'w') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 2)


# In[9]:


# Print Final Output
def printOutput(city_dict, start_time):
    
    # Starting printing format
    print('-------------------------------------------')
    
    # Loop to print each list length
    for city in city_dict:
        print(f'{city}:' + str(len(city_dict[f'{city}']['data']['text'])))
    
    # Final Format Print with runtime
    print('-------------------------------------------')
    print(' --- %s Runtime' % round(time.clock() - start_time,2))


# In[10]:


# Main Execution
def twitterize():
    
    # Setting up statics
    tweet_goal = 20
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





