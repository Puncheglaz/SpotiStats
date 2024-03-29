"""Module for track counting."""
import json
import os
from os import listdir
from os.path import isfile, join


def tracks_count():
    artists_path = "src/aggregator/resources/artists"
    artists_files = [
        file for file in listdir(artists_path) if isfile(join(artists_path, file))
    ]
    if '.DS_Store' in artists_files:
        artists_files.remove('.DS_Store')
    artist_count = 0
    albums_list, tracks_list = [], []
    for artist_file in artists_files:
        with open(f'{artists_path}/{artist_file}', 'r', encoding='utf-8') as artist:
            artist_data = json.load(artist)

            artist_count += 1

            artist_albums = artist_data.get('albums')
            for album in artist_albums:
                album_id = album.get('album_id')
                albums_list.append(album_id)

            artist_tracks = artist_data.get('tracks')
            for track in artist_tracks:
                track_id = track.get('track_id')
                tracks_list.append(track_id)

    # Artists: 2004, Albums: 49820, Tracks: 268643
    print(f'Artists: {artist_count}, Albums: {len(set(albums_list))}, Tracks: {len(set(tracks_list))}')
    return artist_count


def main():
    tracks_count()


if __name__ == '__main__':
    main()
