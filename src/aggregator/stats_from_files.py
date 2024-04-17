"""Module for adding artists stats."""
import datetime
import json

from src.aggregator.stats_utils import (
    change_artist_data,
    change_track_data,
    get_artist_response_template,
    get_artist_albums_ids,
    get_ids_from_file_names
)


def stats_from_files_main(
        timeout, request_count,
        file_path, artist_count, albums_path,
        headers, extensions
):
    """Main function for stats data aggregation."""
    print(f'[T] Time: {datetime.datetime.now()}')

    artist_ids = get_ids_from_file_names(file_path)

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

        change_artist_data(response, artist_id, file_path)

        albums_ids = get_artist_albums_ids(artist_id, file_path)

        artist_albums = get_ids_from_file_names(albums_path)

        for album_id in albums_ids:
            if album_id in artist_albums:
                with open(
                        f'{albums_path}/album-{album_id}.json',
                        mode='r',
                        encoding='utf-8'
                ) as album_file:
                    album_data = json.load(album_file)

                    change_track_data(album_data, artist_id, file_path)
        artist_count += 1


# if __name__ == '__main__':
#     stats_from_files_main(
#         timeout=1,
#         request_count=0,
#         file_path="src/aggregator/resources/artists",
#         artist_count=0,
#         albums_path="src/aggregator/resources/albums"
#         headers=client_headers,
#         extensions=get_artist_stats_extensions
#     )
