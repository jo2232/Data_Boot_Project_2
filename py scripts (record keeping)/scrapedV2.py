
# Dependencies
import json
import time
import os
import requests
import twitter
import numpy as np

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def twitterize():
    analyzer = SentimentIntensityAnalyzer()


    # Loading Keys
    api_dir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
    file_name = os.path.join(api_dir, "api_keys.json")
    data = json.load(open(file_name))

    # Setting Keys
    consumer_key = data['twitter_consumer_key']
    consumer_secret = data['twitter_consumer_secret']
    access_token = data['twitter_access_token']
    access_token_secret = data['twitter_access_token_secret']


    # In[6]:


    # Setting up Auth
    api = twitter.Api(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token_key=access_token,
                    access_token_secret=access_token_secret)


    # In[7]:


    # Tweet Gather function
    def tweetGrab(city):
        
        # Creating return Dict
        tweet_dict = {'text':[], 'coords':[], 'bounding_box':[], 'user':[], 'profile_image_url':[], 'created_at':[], 'comp_sent': [], 'followers_count': []}
        
        # Creating a while loop to run until 100 tweets have been grabbed
        while (len(tweet_dict['text'])<20):
            
            # Call to API - each new call should return new tweets and count against rate-limit
            tweets = api.GetSearch(geocode=[city[1],city[0], '20mi'],return_json=True)

            # Loop to parse tweet and append data needed
            for tweet in tweets['statuses']:
                
                # Appending important data
                tweet_dict['text'].append(tweet['text'])
                tweet_dict['bounding_box'].append(solveBox(tweet['place']['bounding_box']['coordinates']))
                tweet_dict['user'].append(tweet['user']['screen_name'])
                tweet_dict['created_at'].append(tweet['created_at'])
                tweet_dict['followers_count'].append(tweet['user']['followers_count'])
                tweet_dict['comp_sent'].append(analyzer.polarity_scores(tweet['text'])['compound'])
                
                # Creating try loops for variable data that may or may not show up
                try:
                    tweet_dict['coords'].append(tweet['coordinates']['coordinates'])
                except:
                    tweet_dict['coords'].append(tweet['coordinates'])

                try:
                    tweet_dict['profile_image_url'].append(tweet['user']['profile_image_url'])
                except:
                    tweet_dict['profile_image_url'].append('None')
            
            # Sleeping function to allow for new tweets to be fed to API
            time.sleep(20)
            
        # Returning dict of gathered data
        return(tweet_dict)


    # In[11]:


    # Calculating a rough coord based on bounding box
    def solveBox(bounding_box):
        
        # Creating temp dict and variable to return
        coord_dict = {'lat': [], 'lon': []}
        coord_return = []

        # Small loop to append each coord to it's own list to sum
        for coord in bounding_box[0]:
            coord_dict['lat'].append(coord[1])
            coord_dict['lon'].append(coord[0])

        # Appending the sums to a return list
        coord_return.append(np.mean(coord_dict['lon'])) 
        coord_return.append(np.mean(coord_dict['lat']))

        return(coord_return)


    # In[13]:


    # Main execution
    city_gps_dict = {
        'Dallas': [-96.796988, 32.776664],
        'St. Louis': [-90.199404, 38.627003],
        'Los Angeles': [-118.243685, 34.052234],
        'Atlanta': [-84.387982, 33.748995],
        'Chicago': [-87.629798, 41.878114],
        'Miami': [-80.191790, 25.761680],
        'New York': [-74.005973, 40.712775],
        'Kansas City': [-94.578567, 39.099727]
    }

    # Create starting clock point
    start_time = time.clock()

    # Execute script
    text = tweetGrab(city_gps_dict['Dallas'])

    # Printing runtime
    print("--- %s seconds ---" % round(time.clock() - start_time, 2))

return text


# In[14]:




