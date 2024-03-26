"""Module for updating artists stats."""
import datetime
import time

import requests

from auth_credentials import (
    client_headers, get_tracks_extensions
)
from stats_utils import (
    change_artist_data,
    change_track_data,
    get_artist_response_template
)


def main():
    """Main function for stats data updating."""
    print(f'[T] Time: {datetime.datetime.now()}')

    timeout, request_count = 1, 0

    artist_ids = ['00FQb4jTyendYWaN8pK0wa', '0M2HHtY3OOQzIZxrHkbJLT', '4tZwfgrHOc3mvqYlEYSvVi']

    for artist_id in artist_ids:
        response, request_count = get_artist_response_template(
            artist_id,
            timeout,
            request_count
        )
        print(f"Artist Stats {artist_id}  - [*] [Request {request_count} - {response.status_code}]")

        albums_ids = change_artist_data(
            response, artist_id, 'resources/artists'
        )

        for album_id in albums_ids:
            get_album_params = {
                'operationName': 'getAlbum',
                'variables': '{"uri":"spotify:album:' +
                             album_id +
                             '","locale":"","offset":0,"limit":50,"enableAssociatedVideos":false}',
                'extensions': get_tracks_extensions,
            }

            response = requests.get(
                'https://api-partner.spotify.com/pathfinder/v1/query',
                params=get_album_params,
                headers=client_headers,
                timeout=10
            )
            time.sleep(timeout)
            request_count += 1
            print(f"Get Album {album_id}"
                  f"     - [*] [Request {request_count} - {response.status_code}]")

            tracks_data = response.json().get('data').get('albumUnion').get('tracks').get('items')

            change_track_data(tracks_data, artist_id, 'resources/artists')


if __name__ == '__main__':
    main()
