import pandas as pd
from datetime import date
import psycopg2
import config

conn = psycopg2.connect(
        host=config.live_config.host,
        database=config.live_config.database,
        user=config.live_config.user,
        password=config.live_config.password)
conn.autocommit = True
cur = conn.cursor()


csv_file = 'test_list.csv'
df = pd.read_csv(csv_file)
today = date.today().isoformat()


for index, row in df.iterrows():

    print(row['user_id'])
    print(row['follower_count'])
    print('date_updated: ' + str(today) + "\n")

    query = 'INSERT INTO users (twitter_id, follower_count, updated_last) VALUES (%s,%s,%s)'
    cur.execute(query, (row['user_id'], row['follower_count'], today))

# query = 'SELECT * FROM users;'
# cur.execute(query)
# res = cur.fetchall()

# print(res)



# close out connections to the db
cur.close()
conn.close()
