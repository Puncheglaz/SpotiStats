import json
from os import listdir
from os.path import isfile, join

artists_path = "resources/artists"

artists_files = [file for file in listdir(artists_path) if isfile(join(artists_path, file))]

artist_count, albums_count, tracks_count = 0, 0, 0
for artist_file in artists_files:
    with open(f'resources/artists/{artist_file}', 'r', encoding='utf-8') as artist:
        artist_data = json.load(artist)

        artist_count += 1

        artist_albums = artist_data.get('albums')
        for album in artist_albums:
            albums_count += 1

        artist_tracks = artist_data.get('tracks')
        for track in artist_tracks:
            tracks_count += 1

# Artists: 2005, Albums: 50292, Tracks: 269736
print(f'Artists: {artist_count}, Albums: {albums_count}, Tracks: {tracks_count}')
