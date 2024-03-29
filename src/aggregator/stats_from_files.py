"""Module for adding artists stats."""
import datetime
import json
from os import listdir
from os.path import isfile, join

from src.aggregator.stats_utils import (
    change_artist_data,
    change_track_data,
    get_artist_response_template
)


def stats_from_files_main(
        artists_path, timeout, request_count,
        file_path, artist_count, albums_path,
        headers, extensions
):
    """Main function for stats data aggregation."""
    print(f'[T] Time: {datetime.datetime.now()}')

    artists_files_list = listdir(artists_path)
    # artists_files_list.remove('.DS_Store')
    artist_ids = [
        file.split('.')[0].split('-')[1] for file in artists_files_list if isfile(
            join(
                artists_path,
                file
            )
        )
    ]

    for artist_id in artist_ids[artist_count:]:
        response, request_count = get_artist_response_template(
            artist_id=artist_id,
            timeout=timeout,
            request_count=request_count,
            headers=headers,
            extensions=extensions
        )
        print(
            f"Artist Stats {artist_id}"
            f"  - [*] [Request {request_count}"
            f" - {response.status_code}] - Number {artist_count}"
        )

        albums_ids = change_artist_data(
            response, artist_id, file_path
        )

        for album_id in albums_ids:
            artist_albums = [
                file.split('.')[0].split('-')[1] for file in listdir(
                    albums_path
                ) if isfile(
                    join(
                        albums_path,
                        file
                    )
                )
            ]
            if album_id in artist_albums:
                with open(
                        f'{albums_path}/album-{album_id}.json',
                        mode='r',
                        encoding='utf-8'
                ) as album_file:
                    album_data = json.load(album_file)

                    tracks_data = album_data.get(
                        'data'
                    ).get('albumUnion').get('tracks').get('items')

                    change_track_data(tracks_data, artist_id, file_path)
        artist_count += 1


# if __name__ == '__main__':
#     stats_from_files_main(
#         artists_path="src/aggregator/resources/artists",
#         timeout=1,
#         request_count=0,
#         file_path="src/aggregator/resources/artists",
#         artist_count=0,
#         albums_path="src/aggregator/resources/albums"
#         headers=client_headers,
#         extensions=get_artist_stats_extensions
#     )
