"""Module for stats adding and updating utils."""
import json
import time
from collections import OrderedDict
from os import listdir
from os.path import isfile, join

import requests


def change_artist_data(response, artist_id, file_path):
    """Util function for artists stats data aggregation or updating."""
    artist_stats = response.json().get('data').get('artistUnion').get('stats')

    with open(
            f'{file_path}/artist-{artist_id}.json',
            mode='r+',
            encoding='utf-8'
    ) as artist_file:
        data = json.load(artist_file, object_pairs_hook=OrderedDict)
        data['followers'] = artist_stats.get('followers')
        data['monthly_listeners'] = artist_stats.get('monthlyListeners')
        data['world_rank'] = artist_stats.get('worldRank')
        data['top_cities'] = artist_stats.get('topCities').get('items')
        artist_file.seek(0)
        json.dump(
            data,
            artist_file,
            indent=4,
            sort_keys=False,
            ensure_ascii=False
        )
        artist_file.truncate()


def change_track_data(response, artist_id, file_path):
    """Util function for track stats data aggregation or updating."""
    tracks_data = response.get('data').get('albumUnion').get('tracks').get('items')
    path = f'{file_path}/artist-{artist_id}.json'

    for track in tracks_data:
        track_data = track.get('track')
        track_id = track_data.get('uri').split(':')[2]
        track_playcount = track_data.get('playcount')

        with open(
                file=path,
                mode='r+',
                encoding='utf-8'
        ) as artist_file:
            data = json.load(
                artist_file,
                object_pairs_hook=OrderedDict
            )
            for artist_track in data.get('tracks'):
                if artist_track.get('track_id') == track_id:
                    artist_track['playcount'] = track_playcount
            artist_file.seek(0)
            json.dump(
                data,
                artist_file,
                indent=4,
                sort_keys=False,
                ensure_ascii=False
            )
            artist_file.truncate()


def get_artist_response_template(artist_id, timeout, request_count, headers, extensions):
    """Util function for taking artist response template."""
    get_artist_stats_params = {
        'operationName': 'queryArtistOverview',
        'variables': '{"uri":"spotify:artist:' +
                     artist_id +
                     '","locale":"","includePrerelease":true,"enableAssociatedVideos":false}',
        'extensions': extensions,
    }

    response = requests.get(
        'https://api-partner.spotify.com/pathfinder/v1/query',
        params=get_artist_stats_params,
        headers=headers,
        timeout=10
    )
    time.sleep(timeout)
    request_count += 1

    return response, request_count


def get_artist_albums_ids(artist_id, file_path):
    """Util function for taking artist albums ids."""
    with open(
            f'{file_path}/artist-{artist_id}.json',
            mode='r',
            encoding='utf-8'
    ) as artist_file:
        data = json.load(artist_file)

    artist_albums = data.get('albums')
    albums_ids = []
    for album in artist_albums:
        albums_ids.append(album.get('album_id'))

    return albums_ids


def get_ids_from_file_names(files_path):
    """Util function for taking ids from files names by files path."""
    files_list = listdir(files_path)
    if '.DS_Store' in files_list:
        files_list.remove('.DS_Store')
    files_ids = [
        file.split('.')[0].split('-')[1] for file in files_list if isfile(
            join(
                files_path,
                file
            )
        )
    ]

    return files_ids


# if __name__ == '__main__':
#     response, request_count = get_artist_response_template(
#         artist_id='0M2HHtY3OOQzIZxrHkbJLT',
#         timeout=1,
#         request_count=0,
#         headers=client_headers,
#         extensions=get_artist_stats_extensions
#     )
#     print(response)
