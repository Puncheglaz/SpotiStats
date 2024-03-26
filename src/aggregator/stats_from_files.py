"""Module for adding artists stats."""
import datetime
import json
from os import listdir
from os.path import isfile, join

from stats_utils import (
    change_artist_data,
    change_track_data,
    get_artist_response_template
)


def main():
    """Main function for stats data aggregation."""
    print(f'[T] Time: {datetime.datetime.now()}')

    timeout, request_count = 1, 0

    artists_path = "resources/artists"
    artist_ids = [
        file.split('.')[0].split('-')[1] for file in listdir(
            artists_path
        ) if isfile(
            join(
                artists_path,
                file
            )
        )
    ]

    artist_count = 1645
    for artist_id in artist_ids[1645:]:
        response, request_count = get_artist_response_template(
            artist_id,
            timeout,
            request_count
        )
        print(
            f"Artist Stats {artist_id}"
            f"  - [*] [Request {request_count}"
            f" - {response.status_code}] - Number {artist_count}"
        )

        albums_ids = change_artist_data(
            response, artist_id, 'resources/artists'
        )

        for album_id in albums_ids:
            # print(f"Get Album {album_id}")

            with open(
                    f'resources/albums/{album_id}.json',
                    mode='r',
                    encoding='utf-8'
            ) as album_file:
                album_data = json.load(album_file)

                tracks_data = album_data.get(
                    'data'
                ).get('albumUnion').get('tracks').get('items')

                change_track_data(tracks_data, artist_id, 'resources/artists')
        artist_count += 1


if __name__ == '__main__':
    main()
