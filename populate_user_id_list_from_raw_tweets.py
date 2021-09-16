import os
import pandas as pd


def populate_csv(csv_file='user_id_list.csv'):
	
	#import user_id_list.csv and start iterating over each entry
	
	users = pd.read_csv(csv_file)
	
		
	print(users.head())
	
	latest_tweets = []

	for index, row, in users.iterrows():
		# print(row['user_id'])
		latest = find_user_in_raw_tweets(row['user_id'])

		users.at[index, 'date_last_read'] = latest

	print('\n')
	print('...done')
	users.to_csv(csv_file, sep=',', encoding='utf-8', index=False)



	return
	
def find_user_in_raw_tweets(user_id):
	
	# print("Populating")
	# print(os.getcwd())
	raw_tweet_dir = r'./raw_tweets'
	
	dateDirs = os.listdir(raw_tweet_dir)
	
	dateDirs.sort()
	dateDirs.reverse()


	# print(dateDirs)

	for dateFolder in dateDirs:
		dateFolderPath = os.path.join(raw_tweet_dir, dateFolder)
		if os.path.isdir(dateFolderPath):

		# print(dateFolderPath)
			dateFolderPathLen = len(os.listdir(dateFolderPath))

			user_tweet_file = str(user_id) + "_tweets.csv"
			user_tweet_file_path = os.path.join(dateFolderPath, user_tweet_file)

			if os.path.isfile(user_tweet_file_path):
				user_tweet_list = pd.read_csv(user_tweet_file_path)
				if (len(user_tweet_list) > 0):
					# print(len(user_tweet_list))
					latest_tweet_id = user_tweet_list.iloc[0]['id']
					return latest_tweet_id

			# print(dateFolderPathLen)

	
	
	return 



if __name__ == ("__main__"):
	choice = input("Would you like to generate user id list based on raw tweets? (y/n): ")

	if choice == "y":
		populate_csv()
	else:
		print("Exiting")
