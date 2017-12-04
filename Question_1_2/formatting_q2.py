
COL_NAMES = ['user_name', 'password', 'keyword(name)', 'keyword(lname)', 'keyword(color)', 'event', 'event data']

def print_formatting(rows, colnames=COL_NAMES):
    
    format_str = '{:<15} {:<15} {:<15} {:<15} {:<25} {:<15} {}'
    header = format_str.format(*colnames)
    print(header)
    print("-" * len(header))
    for row in rows:
        print(format_str.format(*row))

