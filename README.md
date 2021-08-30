### Twitter Scraper
### Trace DeLange - 08-26-2021

This project was developed in parallel with the following repositories:

 - Money Talks Sinatra API
 - Money talks React Frontend

The purpose of this repositories contents is to first scrape tweets from twitter using the Tweepy API and then aggregate the results into a Postgresql database for use by the Sinatra API.

The purpose of this program is to complete the following functions:
### Gather_tweets
- Read in a list of unique twitter user ID's along with a date indicating the last time a tweet from that user was read.
- Using the Tweepy framework, gather raw text from the users tweet history from the current date to as far back as the most recent date registered.
- Save the raw tweets in a directory featuring the date range associated with the tweets.

### Process_tweets
- Iterate over each tweet and count the frequency of any given ticker symbol that appears in the tweet.
- Establish a connection to the PostgreSQL server and update the relevant tables with the new information.


