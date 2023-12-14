import os
import json

albums = set()
tracks = set()

i = 0

for artist in os.listdir('artists'):
    i += 1
    print(i, artist)

    with open('artists/' + artist) as f:
        data = json.load(f)

    for album in data['albums']:
        albums.add(album['album_id'])

    for track in data['tracks']:
        tracks.add(track['track_id'])