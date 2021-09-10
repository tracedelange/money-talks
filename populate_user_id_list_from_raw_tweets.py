import os
import pandas as pd


def populate_csv(csv_file='user_id_list.csv'):
	
	#import user_id_list.csv and start iterating over each entry
	
	users = pd.read_csv(csv_file)
	
		
	print(users.head())
	
	for index, row, in users.iterrows():
		print(row['user_id'])
		find_user_in_raw_tweets(row['user_id'])


	return
	
def find_user_in_raw_tweets(user_id):
	
	print("Populating")
	
	raw_tweet_dir = r'/home/pi/Code/money-talks/twitter-scraper/raw_tweets'
	
	dateDirs = os.listdir(raw_tweet_dir)
	
	dateDirs.sort()
	dateDirs.reverse()
	
	print(dateDirs)	
	
	
	return 



if __name__ == ("__main__"):
	choice = input("Would you like to generate user id list based on raw tweets? (y/n): ")

	if choice == "y":
		populate_csv()
	else:
		print("Exiting")
