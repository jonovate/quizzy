import json
import traceback
from pprint import pprint

import pymongo

from formatting_q2 import print_formatting


def present_events(events_collection):
    mongo_events = events_collection.find({})

    formatted = map(lambda x: (
        x['_user']['user_name'],
        x['_user']['password'],
        x['__name'],
        x['__last_name'],
        x['__color'],
        x['event_type'],
        json.dumps({key: x[key] for key in x if not key.startswith(
            '_') and key != 'event_type'})
    ), mongo_events)

    print_formatting(formatted)

if __name__ == '__main__':

    client = None
    try:
        print('..Connecting to Mongo...')
        #Would secure this better if had more time
        client = pymongo.MongoClient('mongodb://localhost:27017/')

        db = client.events
        events = db.events_collection

        present_events(events)

    except (Exception) as error:
        traceback.print_exc()
    finally:
        if client is not None:
            client.close()
            print('..DB closed.')
