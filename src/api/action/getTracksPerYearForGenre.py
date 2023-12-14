import random

def execute(conn, data):
    try:

        random.seed(data)

        data = [
            {'year': y, 'count': random.randint(10**3, 10**6)} for y in range(2010, 2024)
        ]

    except KeyError as e:
        return 'malformed json: no such key ' + str(e), 500

    return data, 200