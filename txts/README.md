# Data_Boot_Project_2


## 

Project Statement: Our project will be to build a twitter analyzer that takes in a term or hashtag, returns location information plotted on a map, an analysis of the tweets,
analyze sentiment analysis and compare it to popularity of the tweet. The app will also search and return news articles and display a gauge of the general
composite sentiment analysis.

## To-Do

	-Tweepy API -- Grab geo-data, text, sentiment analysis, tweet popularity metrics. 
	-Google News Scrape -- will search google news for 10-15?? popular news events related to the tweet search term we are analyzing.
	-Flask API -- This will call both Twitter and Google API Python scripts and load results to the Mongo database.
	-MongoDB/SQL -- Will hold twitter and google data
	-Javascript -- Will use to load in MongoDB data and create visuals:
		1. Geographic Map (leaflet?) that plots location of tweets containing search term
		2. Page returning news articles and composite sentiment Gauge using the c3.js library
		3. Scatter plot showing (at least) individual sentiment analysis vs tweet popularity
	-HTML - TBD how many pages we will use to display/organize our data.
 Added 4/26
 	-Error handling on twitter text scrape to eliminate dupes: Christian
	-Re-wrap scraped3 into a python script: Christian
	-Build a dropdown for cities and zoom to that city OR do not pass city, grab all cities and display and allow user to search: 
	-Get Jinja to work and display articles: Jeff
	-Work on plotly graph for twitter followers: Jeff


## Due April 24th (Tuesday)

	You will need to create a 1 page proposal. The proposal should include:
	-A brief articulation of your chosen topic and rationale
	-A link to your dataset(s) and a screenshot of the metadata if it exists.
	-3-4 screenshots of relevant "inspiring" visualizations that frame your creative fodder
	-A sketch of the final design
	-A link to the primary GitHub repository you'll be housing your work in

## Presentation. May 1st:





### Input box -> Sent analysis -> mapping & plotting -> display to page
### Input box -> Google Scrape -> display to page
