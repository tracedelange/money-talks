#Trace DeLange
#08/30/2021
#Script used to delete any tables in database that only contain one row of data.

import psycopg2
import config
from psycopg2 import sql
import email_report
from time import process_time

def clean_db():

    start_time = process_time()

    #Establish DB connection and retreive all table names
    conn = psycopg2.connect(
        host=config.live_config.host,
        database=config.live_config.database,
        user=config.live_config.user,
        password=config.live_config.password)
    conn.autocommit = True
    cur = conn.cursor()

    table_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='public'"

    cur.execute(table_query)
    table_names = cur.fetchall()


    drop_count = 0
    # For each table name, execute a query to determine the number of rows in the table:
    for table_name in table_names:



        count_query = sql.SQL("SELECT count(*) AS exact_count FROM public.{}").format(sql.Identifier(table_name[0]))

        cur.execute(count_query, table_name)
        table_count = cur.fetchall()



        if table_count[0][0] < 5: #If table rows are below threshold, in this case below 2, drop them from the db
            print(table_name[0])
            # print(str(table_count[0][0]) + '\n')

            drop_table = sql.SQL("DROP TABLE public.{}").format(sql.Identifier(table_name[0]))
            cur.execute(drop_table, table_name)
            drop_count += 1
            print(drop_count)




    cur.close()
    conn.close()

    end_time = process_time()

    total_time = end_time - start_time

    report = """

    DB Cleaning process complete.

    Start time: %s
    End time: %s
    Total processing time: %s

    ------------------------------------------

    Number of tables removed: %s

    """ % (start_time, end_time, total_time, drop_count)

    email_report.email_report(report, 'tracedelange@me.com', 'DB Clean-up')

    return


# close out connections to the db

if __name__ == "__main__":

    print('Cleaning DB...')

    clean_db()



# Get all table names in DB:
# SELECT TABLE_NAME 
# FROM INFORMATION_SCHEMA.TABLES
# WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='public' 