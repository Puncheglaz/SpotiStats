import json
import random
import requests
from server_vars import server_address, server_port

with open(f'resources/artists/artist-1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

    data['artist_id'] = str(random.randint(0, 100000000)) + chr(random.randint(60, 100))
    data['name'] += str(random.randint(0, 100))
    print(data)

    header = {
        'Content-Type': 'application/json'
    }

    json_string = json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )
    response = requests.post(
        f'http://{server_address}:{server_port}/saveArtist',
        headers=header,
        data=json_string
    )
    print(response.text)
