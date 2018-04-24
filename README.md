# Data_Boot_Project_2


## 

Project Statement: Our project will be to build a twitter analyzer that takes in a specific set of coordinates, or city name, and  returns information regarding the tweet and it's overal sentiment. The app will also search and return news articles and display a gauge of the general composite sentiment analysis. Our hope is that by choosing an area and gathering tweets from it, we can gauge the general sentiment of a city - And if an event is big enough, we may be able to gauge general sentiment of a city for a particular topic (NBA Finals, Active Shooter situation, Hurricanes, etc)

## To-Do

	-Twitter API -- Grab geo-data, text, sentiment analysis, tweet popularity metrics. 
	-Google News Scrape -- will search google news for 10-15?? popular news events related to the tweet search term we are analyzing.
	-Flask API -- This will call both Twitter and Google API Python scripts and load results to the Mongo database.
	-MongoDB/SQL -- Will hold twitter and google data
	-Javascript -- Will use to load in MongoDB data and create visuals:
		1. Geographic Map (leaflet?) that plots location of tweets containing search term
		2. Page returning news articles and composite sentiment Gauge using the c3.js library
		3. Scatter plot showing (at least) individual sentiment analysis vs tweet popularity
	-HTML - TBD how many pages we will use to display/organize our data.


## Due April 24th (Tuesday)

	You will need to create a 1 page proposal. The proposal should include:
	-A brief articulation of your chosen topic and rationale
	-A link to your dataset(s) and a screenshot of the metadata if it exists.
	-3-4 screenshots of relevant "inspiring" visualizations that frame your creative fodder
	-A sketch of the final design
	-A link to the primary GitHub repository you'll be housing your work in

## Presentation. May 1st:





### Input box -> Sent for analysis -> mapping & plotting -> display to page
### Input box -> Google Scrape -> display to page
