"""Returns a list of colors"""
def gen_colors():
    with open('colors.txt') as f:
        lines = list(map(str.title, f.read().splitlines()))
    return lines

def gen_event_types():
    return ['Thanksgiving', 'Potluck', 'Birthday']
def gen_names():
    return ['Jon Jay', 'Sandy Ess', 'Tom Tee', 'Tina Tee']
def gen_foods():
    return ['Casserole', 'Key Lime Tarts', 'BBQ', 'Salad']

if __name__ == '__main__':
    print(gen_colors())
