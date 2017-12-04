import json
import random
import traceback

import nameparser
import psycopg2
import psycopg2.extras

import generate_data


def handle_colors(curr, conn):
  
    curr.execute('SELECT COUNT(*) FROM colors')
    if 0 == curr.fetchone()[0]:
        colors = generate_data.gen_colors()
        curr.executemany('INSERT INTO colors(color_name) VALUES (%s)',
                          [[color] for color in colors])
        conn.commit()
        print('Inserted %d colors' % curr.rowcount)
    else:
        print('Colors exist')

    curr.execute('SELECT color_name,id FROM colors')
    results = dict(curr.fetchall())

    return results

def handle_event_types(curr, conn):

    curr.execute('SELECT COUNT(*) FROM event_types')
    if 0 == curr.fetchone()[0]:
        events = generate_data.gen_event_types()
        curr.executemany('INSERT INTO event_types(event_name) VALUES (%s)',
                          [[ev] for ev in events])
        conn.commit()
        print('Inserted %d event types' % curr.rowcount)
    else:
        print('Event Types exist')

    curr.execute('SELECT event_name,id FROM event_types')
    results = dict(curr.fetchall())

    return results

def perform_inserts(curr, conn, color_dict, event_type_dict, names, foods):
    
    with open('events.json') as eventsfile:
        events_all = json.load(eventsfile)

        counter = 0

        for event_type, events in events_all.items():
            
            normalized_tpls, json_tpls = list(), list()

            for event in events:
                tpl_n = ( 
                    event_type_dict[event_type],
                    'jhoweyusername',
                    'jhoweypassword',
                    color_dict[random.choice(list(color_dict.keys()))],
                    event['name'],
                    event['food'],
                    event['confirmed'],
                    event['signup_date'],
                )
                normalized_tpls.append(tpl_n)

                tpl_j = (
                    event_type,
                    'jhoweyusername',
                    'jhoweypassword',
                    event['name'],
                    nameparser.HumanName(event['name']).last,
                    random.choice(list(color_dict.keys())),
                    json.dumps(event),
                )
                json_tpls.append(tpl_j)
            qry_n = 'INSERT INTO events (event_type_id, user_name, password, color_id, name, food, confirmed, signup_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            curr.executemany(qry_n, normalized_tpls)
            counter += curr.rowcount
            conn.commit()

            qry_j = 'INSERT INTO events_json (event_type, user_name, password, metadata_name, metadata_last_name, metadata_color, event) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            curr.executemany(qry_j, json_tpls)
            conn.commit()

        print('Inserted %d events x2' % counter)

if __name__ == '__main__':

    conn = None
    try:
        print('..Connecting to PG...')
        #Would secure this better if had more time
        conn = psycopg2.connect(host="localhost", port="5432", database="events", user="usr_question1", password="goGO99")
        curr = conn.cursor()

        color_dict = handle_colors(curr, conn)
        event_type_dict = handle_event_types(curr, conn)
        names = generate_data.gen_names()
        foods = generate_data.gen_foods()

        perform_inserts(curr, conn, color_dict, event_type_dict, names, foods)

    except (Exception, psycopg2.DatabaseError) as error:
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()
            print('..DB closed.')
