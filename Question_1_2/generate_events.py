import datetime
import itertools
import json
import random

import radar

import generate_data


def gen_events():
    events = generate_data.gen_event_types()
    names = generate_data.gen_names()
    foods = generate_data.gen_foods()

    output = {}

    for event_name in events:
        random.shuffle(foods)

        output[event_name] = list()
        tpl = tuple(zip(names, foods))
        for name, food in tpl:
            event = {
                'name': name,
                'food': food,
                'confirmed': random.choice([True, False]),
                'signup_date': radar.random_datetime(start='2017-06-01', stop='2019-12-31').strftime('%Y-%m-%d')
            }
            output[event_name].append(event)

    return output

if __name__ == '__main__':
    output = gen_events()
    
    print('Writing file as events.json')
    with open('events.json', 'w') as eventsjson:
        json.dump(output, eventsjson)
    #print(json.dumps(output, indent=4))
