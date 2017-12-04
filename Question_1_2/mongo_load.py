import json
import random
import traceback
from pprint import pprint

import nameparser
import pymongo

import generate_data


def setup_indexes(db):
    db.event_collection.create_index([('__name', pymongo.ASCENDING)], unique=False)
    db.event_collection.create_index([('__last_name', pymongo.ASCENDING)], unique=False)
    db.event_collection.create_index([('__color', pymongo.ASCENDING)], unique=False)

def perform_inserts(events_collection):    
    colors = generate_data.gen_colors()

    with open('events.json') as eventsfile:
        events_all = json.load(eventsfile)

        bulk_add = list()
        for event_type, events in events_all.items():
            
            #Enrich
            for event in events:
                event['event_type'] = event_type

                event['_user'] = {'user_name': 'jhoweyusername', 'password': 'jhoweypassword'}

                #Add fields for our keyword indexing later
                event['__color'] = random.choice(colors)
                event['__name'] = event['name']
                event['__last_name'] = nameparser.HumanName(event['name']).last
                bulk_add.append(event)

        result = events_collection.insert_many(bulk_add)

        print('Inserted %d events' % len(result.inserted_ids))


if __name__ == '__main__':

    client = None
    try:
        print('..Connecting to Mongo...')
        #Would secure this better if had more time
        client = pymongo.MongoClient('mongodb://localhost:27017/')

        db = client.events
        events = db.events_collection
        #print(list(map(pprint, events.find({'event_type': 'Thanksgiving'}))))

        if len(list(db.event_collection.index_information())) <= 1:
            setup_indexes(db)
        if not events.count():
            perform_inserts(events)


    except (Exception) as error:
        traceback.print_exc()
    finally:
        if client is not None:
            client.close()
            print('..DB closed.')
