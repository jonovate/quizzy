import json
import random
import traceback

import nameparser
from neo4jrestclient.client import GraphDatabase

import generate_data


def build(gdb):

    if gdb.labels:
        print('Labels, Nodes, and Relationships already loaded')
        return
    
    lblperson = gdb.labels.create('Person')
    gdbnames = dict(map(lambda x: (x, lblperson.create(name=x, last_name=nameparser.HumanName(x).last)),
                        generate_data.gen_names()))

    colors = generate_data.gen_colors()
    lblevent = gdb.labels.create('Event')
    gdbevent_types = dict(map(lambda x: (x, lblevent.create(name=x,
                                                            colors=random.sample(colors, random.randint(1, 3)),
                                                            user=json.dumps({'user_name': 'jhoweyusername', 'password': 'jhoweypassword'}))),
                              generate_data.gen_event_types()))
    lblfoods = gdb.labels.create('Food')
    gdbfoods = dict(map(lambda x: (x, lblfoods.create(name=x)),
                        generate_data.gen_foods()))


    with open('events.json') as eventsfile:
        events_all = json.load(eventsfile)

        for event_type, events in events_all.items():
            for event in events:
                         
                person = gdbnames[event['name']]
                cur_event = gdbevent_types[event_type] #Avoid renaming to event as its loop var :)
                food = gdbfoods[event['food']]

                person.relationships.create('Attends', cur_event, confirmed=event['confirmed'], brought=event['food'])
                person.relationships.create('Brings', food, signup_date=event['signup_date'], attended=event_type)

if __name__ == '__main__':

    gdb = None
    try:
        print('..Connecting to Neo4J...')
        #Would secure this better if had more time
        gdb = GraphDatabase('http://localhost:7474/db/data/', username='neo4j', password='neo4j2')

        build(gdb)
    except (Exception) as error:
        traceback.print_exc()
