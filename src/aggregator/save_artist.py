import json
import time
import random
import requests
from server_vars import server_address, server_port

ids = ['00FQb4jTyendYWaN8pK0wa', '0M2HHtY3OOQzIZxrHkbJLT']

for artist_id in ids:
    with open(f'resources/artists/artist-{artist_id}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        header = {
            'Content-Type': 'application/json'
        }

        json_string = json.dumps(
            data
        )
        response = requests.post(
            f'http://{server_address}:{server_port}/saveArtist',
            headers=header,
            data=json_string
        )
        print(f"{response.text} - Status Code: {response.status_code}")
        time.sleep(1)
