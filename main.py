#!/usr/bin/env/python3.7

from typing import Dict
import tweepy
import pandas as pd
import datetime
import csv
# from datetime import date
from datetime import datetime, date
from time import process_time
from resources import *
import os
import config
import psycopg2
import email_report
from config import twitter_config



#set the working directory to the current directory in case this is being called from outside the directory, like from a cronjob



script_dir = os.path.dirname(os.path.realpath("/home/pi/Code/money-talks/twitter-scraper/main.py"))
os.chdir(script_dir)


email_report.email_report('Main.py Activated via cron', 'tracedelange@me.com', "test")


process_start = datetime.now()
start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

today = date.today().isoformat()
print('Imports successful')


consumer_key = twitter_config.consumer_key
consumer_secret = twitter_config.consumer_secret
access_token = twitter_config.access_token
access_token_secret = twitter_config.access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)

print('Twitter authentication successful \n')

print('Reading in user IDs...')

#/home/pi/Code/money-talks/twitter-scraper/user_id_list.csv


csv_file = '/home/pi/Code/money-talks/twitter-scraper/user_id_list.csv'

df = pd.read_csv(csv_file)
df.columns = ['user_id', 'follower_count', 'date_last_read']

print('Users_ids obtained')


stats = {} #initialize the stats object


def contains_ticker(text): ##good candidate to be moved to resources and imported
    for word in text:
        if word[0] == '$':
            return True
    return False

#number of users iterated over:
stats['users_checked'] = len(df)
#total number of tweets scraped over each user
stats['total_collected'] = 0
stats['user_count'] = 0

for index, row in df.iterrows():
    # print(type(row['date_last_read']))

    try:
        # print(int(row['date_last_read']))
        since = int(row['date_last_read'])
    except:
        #not an int, date obj, default to something
        since = 1
    #     
    print('Downloading user ' + str(row['user_id']) + ' tweets')
#     #Generate and save a list of user tweets as a csv in the raw_tweets dir
    target_user_id = row['user_id']

#     # initialize a list to hold all the tweepy Tweets
    alltweets = []

#     # make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(id=target_user_id, count=200, since_id=since)
    except:
        print('Skipping protected user... OR no new tweets to collect...')
        continue

    # print(len(new_tweets))
#     # save most recent tweets
    alltweets.extend(new_tweets)
    
    try:
#         # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
    except:
        print('Indexing error getting oldest tweet, moving onto next user...')
        continue
        
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:


#         # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(id=target_user_id, count=200, max_id=oldest, since_id=since)

#         # save most recent tweets
        alltweets.extend(new_tweets)

#         # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1


    final = []
    for tweet in alltweets:
        if contains_ticker(tweet.text):
            final.append(tweet)

    #     # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in final]

    stats['total_collected'] += len(outtweets)

    print(str(len(outtweets)) + " Tweets saved...")
    #check to see if path does not exist, if so, create it

    if not os.path.exists('raw_tweets/{}'.format(today)):
        os.makedirs('raw_tweets/{}'.format(today))

    # write the csv
    with open("raw_tweets/{}/{}_tweets.csv".format(today, target_user_id), 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)   
        
    # print(outtweets[0])
    # print(outtweets[-1])
    print('Tweets saved to /raw_tweets')

    if len(outtweets) > 0:
        df.loc[df.user_id == row['user_id'], 'date_last_read'] = outtweets[0][0]

    # print('\n')
    print('...done')
    df.to_csv('test_list.csv', sep=',', encoding='utf-8', index=False)
    
    stats['user_count'] += 1
    
    p = int(round(((stats['user_count'] / len(df)) * 100), 0))
    loading_string = '/' + ('X' * (p)) + ('-' * (100 - p)) + '/'
    print(loading_string)


# print("Oldest: "  + str(oldest))
#update the datatable with the tweet id as the most recent entry and write the csv.



print('New tweets saved to directory, continuing to process mentions and push to database...')

directory = "raw_tweets/{}/".format(today)

conn = psycopg2.connect(
        host=config.live_config.host,
        database=config.live_config.database,
        user=config.live_config.user,
        password=config.live_config.password)
conn.autocommit = True
cur = conn.cursor()

file_count = 0
total_files = len(os.listdir(directory))
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # if os.path.isfile(filename):
    df = get_df(f)

    if len(df) == 0: #if the dataframe is empty, skip the iteration
        print("No tweets for user, moving to next... \n")
        file_count += 1
        continue

    
    user_id = filename.split('_')[0]

    user_follower_count = get_follower_count(user_id, cur)[0][0]


    dic = gen_master_dic(df)

    print('\n')
    print("User ID: " + str(user_id))
    print("User Follower Count: " + str(user_follower_count))
    print("Users processed: " + str(file_count))

    p = int(round(((file_count / total_files) * 100), 0))
    loading_string = '/' + ('X' * (p)) + ('-' * (100 - p)) + '/'
    print(loading_string)


    for key in dic.keys():
        for dateKey in dic[key].keys():
            # print(dateKey)
            # print(dic[key][dateKey])
            count = dic[key][dateKey]
            # print(count)
            dic[key][dateKey] = [count, count*user_follower_count]

            # print(dic[key][dateKey])

    # for entry in dic.keys():
    #     print(entry)

    # print(dic)
	
    upsert_database(dic, cur)
    file_count += 1



# close out connections to the db
cur.close()
conn.close()

process_end = datetime.now()
end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

process_timespan = process_end - process_start

report_body = """

Scraping process complete!

Start time: %s
End time: %s
Total processing time: %s

------------------------------------------

Number of users scanned: %s

Total number of mentions collected: %s


""" % (start_time, end_time, (process_timespan.total_seconds)/60, stats['users_checked'], stats['total_collected'])


# Send out message to email address with the stats of the last run:
email_report.email_report(report_body, 'tracedelange@me.com', "Scrape Update " + str(today))


