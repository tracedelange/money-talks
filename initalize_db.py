import psycopg2
from populate_user_table_from_csv import populate_user_table_from_csv
import config

# Create appropriate tables, then call populate_user_table_from_csv:


conn = psycopg2.connect(
        host=config.live_config.host,
        database=config.live_config.database,
        user=config.live_config.user,
        password=config.live_config.password)
conn.autocommit = True
cur = conn.cursor()

query = 'CREATE TABLE IF NOT EXISTS public.users (twitter_id BIGINT primary key, follower_count INTEGER, updated_last DATE);'
cur.execute(query)

query = 'CREATE TABLE IF NOT EXISTS public.date_mentions (date_mention_id SERIAL primary key, date DATE, users INTEGER, ticker_id INTEGER, mentions INTEGER, estimated_outreach INTEGER);'
cur.execute(query)

query = 'CREATE TABLE IF NOT EXISTS public.tickers (ticker_id SERIAL primary key, ticker_name VARCHAR(20));'
cur.execute(query)

populate_user_table_from_csv('user_id_list.csv')

conn.close()
cur.close()
