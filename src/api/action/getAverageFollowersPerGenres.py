def execute(conn, data):
    try:

        data = [
            {"genre": "pop", "followers": 575580},
            {"genre": "dance pop", "followers": 366189},
            {"genre": "house", "followers": 328939},
            {"genre": "teen pop", "followers": 328082},
            {"genre": "electro house", "followers": 327309},
            {"genre": "edm", "followers": 323467},
            {"genre": "pop rap", "followers": 323125},
            {"genre": "pop christmas", "followers": 303698},
            {"genre": "pop rock", "followers": 168562},
            {"genre": "r&b", "followers": 154259},
            {"genre": "big room", "followers": 151126},
            {"genre": "alternative hip hop", "followers": 150749},
            {"genre": "urban contemporary", "followers": 145312},
            {"genre": "progressive electro house", "followers": 143170},
            {"genre": "indie r&b", "followers": 140098},
            {"genre": "indietronica", "followers": 138943},
            {"genre": "permanent wave", "followers": 124323},
            {"genre": "synthpop", "followers": 121304},
            {"genre": "contemporary country", "followers": 120795},
            {"genre": "neo mellow", "followers": 119190}
        ]

    except KeyError as e:
        return 'malformed json: no such key ' + str(e), 500

    return data, 200