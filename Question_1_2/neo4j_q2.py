import json
import traceback

from neo4jrestclient.client import GraphDatabase, Incoming, Outgoing, All

from formatting_q2 import print_formatting

def present_graph_data(gdb):
    lblevent = gdb.labels.get("Event")
    gdbevents = lblevent.all()

    output_tpls = []

    #Must be a way to traverse DFS, TODO
    for event in gdbevents:

        event_type = event.properties['name']
        userobj = json.loads(event.properties['user'])  #Is a string for some reason

        people_iter = event.traverse()

        for person in people_iter:
  
            food_rel = [food for food in person.relationships.outgoing(['Brings'])
                        if food.properties['attended'] == event_type][0]
            food = food_rel.end
            event_rel = [pers for pers in person.relationships.outgoing(['Attends'])
                         if pers.end.id == event.id][0]

            tpl = (
                userobj['user_name'],
                userobj['password'],
                person.properties['name'],
                person.properties['last_name'],
                '/'.join(event.properties['colors'])[:25],
                event_type,
                json.dumps({
                    'name': person.properties['name'],
                    'food': food.properties['name'],
                    'confirmed': event_rel.properties['confirmed'],
                    'signup_date': food_rel.properties['signup_date']
                })
            )
            output_tpls.append(tpl)

    print_formatting(output_tpls)


if __name__ == '__main__':

    gdb = None
    try:
        print('..Connecting to Neo4J...')
        #Would secure this better if had more time
        gdb = GraphDatabase('http://localhost:7474/db/data/', username='neo4j', password='neo4j2')

        present_graph_data(gdb)
    except (Exception) as error:
        traceback.print_exc()

