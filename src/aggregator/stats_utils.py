"""Module for stats adding and updating utils."""
import json
import time
from collections import OrderedDict

import requests

from auth_credentials import (
    client_headers, get_artist_stats_extensions
)


def change_artist_data(response: requests.Response, artist_id):
    """Util function for artists stats data aggregation or updating."""
    artist_stats = response.json().get('data').get('artistUnion').get('stats')

    with open(
            f'resources/artists/artist-{artist_id}.json',
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

    with open(
            f'resources/artists/artist-{artist_id}.json',
            mode='r',
            encoding='utf-8'
    ) as artist_file:
        data = json.load(artist_file)

    artist_albums = data.get('albums')
    albums_ids = []
    for album in artist_albums:
        albums_ids.append(album.get('album_id'))

    return albums_ids


def change_track_data(tracks_data, artist_id):
    """Util function for track stats data aggregation or updating."""
    for track in tracks_data:
        track_data = track.get('track')
        track_id = track_data.get('uri').split(':')[2]
        track_playcount = track_data.get('playcount')

        with open(
                f'resources/artists/artist-{artist_id}.json',
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


def get_artist_response_template(artist_id, timeout, request_count):
    """Util function for taking artist response template."""
    get_artist_stats_params = {
        'operationName': 'queryArtistOverview',
        'variables': '{"uri":"spotify:artist:' +
                     artist_id +
                     '","locale":"","includePrerelease":true,"enableAssociatedVideos":false}',
        'extensions': get_artist_stats_extensions,
    }

    response = requests.get(
        'https://api-partner.spotify.com/pathfinder/v1/query',
        params=get_artist_stats_params,
        headers=client_headers,
        timeout=10
    )
    time.sleep(timeout)
    request_count += 1

    return response, request_count
