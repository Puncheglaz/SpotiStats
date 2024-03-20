"""Module for track counting."""
import json
import os
from os import listdir
from os.path import isfile, join


def tracks_count():
    if '\\'.join(os.getcwd().split('\\')[-3:]) == "SpotiStats\\src\\aggregator":
        ARTISTS_PATH = "resources/artists"
    else:
        ARTISTS_PATH = "src\\aggregator\\resources\\artists"
    print('\\'.join(os.getcwd().split('\\')[-3:]))
    artists_files = [file for file in listdir(ARTISTS_PATH) if isfile(join(ARTISTS_PATH, file))]
    ARTIST_COUNT = 0
    albums_list, tracks_list = [], []
    for artist_file in artists_files:
        with open(f'{ARTISTS_PATH}/{artist_file}', 'r', encoding='utf-8') as artist:
            artist_data = json.load(artist)

            ARTIST_COUNT += 1

            artist_albums = artist_data.get('albums')
            for album in artist_albums:
                album_id = album.get('album_id')
                albums_list.append(album_id)

            artist_tracks = artist_data.get('tracks')
            for track in artist_tracks:
                track_id = track.get('track_id')
                tracks_list.append(track_id)

    # Artists: 2004, Albums: 49820, Tracks: 268643
    print(f'Artists: {ARTIST_COUNT}, Albums: {len(set(albums_list))}, Tracks: {len(set(tracks_list))}')
    return ARTIST_COUNT


def main():
    tracks_count()


# if __name__ == '__main__':
#     main()
