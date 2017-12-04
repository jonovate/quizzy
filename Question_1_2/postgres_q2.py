import json
import random
import traceback
import nameparser

import psycopg2
import psycopg2.extras

def present_events(curr):
    
    curr.execute('SELECT user_name, password, metadata_name as "keyword(name)", metadata_last_name as "keyword(lname)", metadata_color as "keyword(color)",  event_type as "event", event as "event data" FROM events_json')
    results = curr.fetchall()
    colnames = [desc[0] for desc in curr.description]
   
    format_str = '{:<15} {:<15} {:<15} {:<15} {:<25} {:<15} {}'
    header = format_str.format(*colnames) 
    print(header)
    print("-" * len(header))
    for row in results:
        print(format_str.format(*row))

if __name__ == '__main__':

    conn = None
    try:
        print('..Connecting to PG...')
        #Would secure this better if had more time
        conn = psycopg2.connect(host="localhost", port="5432", database="events", user="usr_question1", password="goGO99")
        curr = conn.cursor()

        present_events(curr)


    except (Exception, psycopg2.DatabaseError) as error:
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()
            print('..DB closed.')
