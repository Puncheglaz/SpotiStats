import json
import time
import requests
import datetime

from collections import OrderedDict
from auth_credentials import (
    client_headers, get_tracks_extensions, get_artist_stats_extensions
)


def main():
    print(f'                                         [T] Time: {datetime.datetime.now()}')

    timeout, request_count = 1, 0

    artist_ids = ['00FQb4jTyendYWaN8pK0wa', '0M2HHtY3OOQzIZxrHkbJLT', '4tZwfgrHOc3mvqYlEYSvVi']

    for artist_id in artist_ids:
        get_artist_stats_params = {
            'operationName': 'queryArtistOverview',
            'variables': '{"uri":"spotify:artist:' +
                         artist_id + '","locale":"","includePrerelease":true,"enableAssociatedVideos":false}',
            'extensions': get_artist_stats_extensions,
        }

        response = requests.get(
            'https://api-partner.spotify.com/pathfinder/v1/query',
            params=get_artist_stats_params,
            headers=client_headers
        )
        time.sleep(timeout)
        request_count += 1
        print(f"Artist Stats {artist_id}  - [*] [Request {request_count} - {response.status_code}]")

        artist_stats = response.json().get('data').get('artistUnion').get('stats')

        with open(f'resources/artists/artist-{artist_id}.json', 'r+', encoding='utf-8') as artist_file:
            data = json.load(artist_file, object_pairs_hook=OrderedDict)
            data['followers'] = artist_stats.get('followers')
            data['monthly_listeners'] = artist_stats.get('monthlyListeners')
            data['world_rank'] = artist_stats.get('worldRank')
            data['top_cities'] = artist_stats.get('topCities').get('items')
            artist_file.seek(0)
            json.dump(data, artist_file, indent=4, sort_keys=False, ensure_ascii=False)
            artist_file.truncate()

        with open(f'resources/artists/artist-{artist_id}.json', 'r', encoding='utf-8') as artist_file:
            data = json.load(artist_file)

        artist_albums = data.get('albums')
        albums_ids = list()
        for album in artist_albums:
            albums_ids.append(album.get('album_id'))

        for album_id in albums_ids:
            get_album_params = {
                'operationName': 'getAlbum',
                'variables': '{"uri":"spotify:album:' +
                             album_id + '","locale":"","offset":0,"limit":50,"enableAssociatedVideos":false}',
                'extensions': get_tracks_extensions,
            }

            response = requests.get(
                'https://api-partner.spotify.com/pathfinder/v1/query',
                params=get_album_params,
                headers=client_headers
            )
            time.sleep(timeout)
            request_count += 1
            print(f"Get Album {album_id}     - [*] [Request {request_count} - {response.status_code}]")

            tracks_data = response.json().get('data').get('albumUnion').get('tracks').get('items')

            for track in tracks_data:
                track_data = track.get('track')
                track_id = track_data.get('uri').split(':')[2]
                track_playcount = track_data.get('playcount')

                with open(f'resources/artists/artist-{artist_id}.json', 'r+', encoding='utf-8') as artist_file:
                    data = json.load(artist_file, object_pairs_hook=OrderedDict)
                    for artist_track in data.get('tracks'):
                        if artist_track.get('track_id') == track_id:
                            artist_track['playcount'] = track_playcount
                    artist_file.seek(0)
                    json.dump(data, artist_file, indent=4, sort_keys=False, ensure_ascii=False)
                    artist_file.truncate()


if __name__ == '__main__':
    main()
