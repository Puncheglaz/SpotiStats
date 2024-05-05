"""Module aggregator to collect track and artist data from Spotify."""
import datetime
import json
import time

import requests
from loguru import logger

from src.aggregator.auth_credentials import client_id, client_secret, token_type, access_token
from src.aggregator.classes.album import Album
from src.aggregator.classes.artist import Artist
from src.aggregator.classes.track import Track

token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}


def aggregate(low, high):
    """Main function for data aggregation."""
    logger.info(f'[T] Time: {datetime.datetime.now()}')

    timeout, request_count = 2, 0

    headers = {
        'Authorization': f'{token_type}  {access_token}',
    }

    id_file_name = 'artists-ids-list.json'
    with open(
            f'src/aggregator/resources/{id_file_name}',
            mode='r',
            encoding='utf-8'
    ) as file:
        artists_ids = json.load(file)

    for artist_id in artists_ids[low:high]:
        # 1 request
        response = requests.get(
            f'https://api.spotify.com/v1/artists/{artist_id}',
            headers=headers,
            timeout=10
        )
        time.sleep(timeout)
        request_count += 1
        logger.info(f"[*] [Request {request_count} - {response.status_code}]")

        if response.status_code != 200:
            logger.warning('Token expired!')
            # 2 request (potential)
            response = requests.post(
                'https://accounts.spotify.com/api/token',
                data=token_data,
                timeout=10
            )
            time.sleep(timeout)
            request_count += 1
            logger.info(f"[*] [Request {request_count} - {response.status_code}]")

            headers['Authorization'] = (
                f"{response.json().get('token_type')}"
                f"  {response.json().get('access_token')}"
            )

            # 3 request (potential)
            response = requests.get(
                f'https://api.spotify.com/v1/artists/{artist_id}',
                headers=headers,
                timeout=10
            )
            time.sleep(timeout)
            request_count += 1
            logger.info(f"[*] [Request {request_count} - {response.status_code}]")

        artist_info_data = response.json()
        logger.info(f"Get {artist_id} data")
        logger.debug(f"Artist ID: {artist_info_data.get('id')}")
        logger.debug(f"Artist Name: {artist_info_data.get('name')}")
        logger.debug(f"Artist Popularity: {artist_info_data.get('popularity')}")
        logger.debug(f"Artist Genres: {artist_info_data.get('genres')}")
        logger.debug(f"Artist Followers: {artist_info_data.get('followers').get('total')}")

        artist_for_json = Artist(
            artist_id,
            artist_info_data.get('name'),
            artist_info_data.get('popularity'),
            artist_info_data.get('followers').get('total'),
            artist_info_data.get('genres'),
        )

        album_params = {
            'include_groups': 'album',
            'limit': 50,
            'offset': 0,
            'market': 'ES'
        }

        # 4 request
        response = requests.get(
            f'https://api.spotify.com/v1/artists/{artist_id}/albums',
            params=album_params,
            headers=headers,
            timeout=10
        )
        time.sleep(timeout)
        request_count += 1
        logger.info(f"[*] [Request {request_count} - {response.status_code}]")

        if response.status_code != 200:
            logger.warning('Token expired!')

            response = requests.post(
                'https://accounts.spotify.com/api/token',
                data=token_data,
                timeout=10
            )
            time.sleep(timeout)
            request_count += 1
            logger.info(f"[*] [Request {request_count} - {response.status_code}]")

            headers['Authorization'] = (
                f"{response.json().get('token_type')}"
                f"  {response.json().get('access_token')}"
            )

            response = requests.get(
                f'https://api.spotify.com/v1/artists/{artist_id}/albums',
                params=album_params,
                headers=headers,
                timeout=10
            )
            time.sleep(timeout)
            request_count += 1
            logger.info(f"[*] [Request {request_count} - {response.status_code}]")

        artist_albums_ids = []
        artist_albums = response.json().get('items')
        for album in artist_albums:
            artist_albums_ids.append(album.get('id'))

        logger.info(f"Get {artist_id} albums")

        album_params['include_groups'] = 'single'

        # 5 request
        response = requests.get(
            f'https://api.spotify.com/v1/artists/{artist_id}/albums',
            params=album_params,
            headers=headers,
            timeout=10
        )
        time.sleep(timeout)
        request_count += 1
        logger.info(f"[*] [Request {request_count} - {response.status_code}]")

        if response.status_code != 200:
            logger.warning('Token expired!')

            response = requests.post(
                'https://accounts.spotify.com/api/token',
                data=token_data,
                timeout=10
            )
            time.sleep(timeout)
            request_count += 1
            logger.info(f"[*] [Request {request_count} - {response.status_code}]")

            headers['Authorization'] = (
                f"{response.json().get('token_type')}"
                f"  {response.json().get('access_token')}"
            )

            response = requests.get(
                f'https://api.spotify.com/v1/artists/{artist_id}/albums',
                params=album_params,
                headers=headers,
                timeout=10
            )
            time.sleep(timeout)
            request_count += 1
            logger.info(f"[*] [Request {request_count} - {response.status_code}]")

        artist_albums = response.json().get('items')
        for album in artist_albums:
            artist_albums_ids.append(album.get('id'))

        logger.info(f"Get {artist_id} singles")

        total_albums_ids = len(artist_albums_ids)
        logger.info(f'Total albums & singles: {total_albums_ids}')

        several_albums_params = {
            'ids': ''
        }

        # 5 requests above, 55 requests below left
        albums_json, tracks_json = [], []
        id_offset = 20
        for i in range(0, total_albums_ids, id_offset):
            several_albums_params['ids'] = (
                ','.join(artist_albums_ids[i:i + id_offset])
            )
            # max 100 albums or singles = 5 requests (5 * 20)
            response = requests.get(
                'https://api.spotify.com/v1/albums',
                params=several_albums_params,
                headers=headers,
                timeout=10
            )
            time.sleep(timeout)
            request_count += 1
            logger.info(f"[*] [Request {request_count} - {response.status_code}]")

            if response.status_code != 200:
                logger.warning('Token expired!')

                response = requests.post(
                    'https://accounts.spotify.com/api/token',
                    data=token_data,
                    timeout=10
                )
                time.sleep(timeout)
                request_count += 1
                logger.info(f"[*] [Request {request_count} - {response.status_code}]")

                headers['Authorization'] = (
                    f'{response.json().get("token_type")}'
                    f'  {response.json().get("access_token")}'
                )

                response = requests.get(
                    'https://api.spotify.com/v1/albums',
                    params=several_albums_params,
                    headers=headers,
                    timeout=10
                )
                time.sleep(timeout)
                request_count += 1
                logger.info(f"[*] [Request {request_count} - {response.status_code}]")

            album_data = response.json().get('albums')
            for album in album_data:
                logger.info(f"Get Album {album.get('id')}")
                logger.debug("")
                logger.debug(f"Album Name: {album.get('name')}")
                album_id = album.get('id')
                logger.debug(f"Album ID: {album_id}")
                logger.debug(f"Album Type: {album.get('album_type')}")
                logger.debug(f"Album Date: {album.get('release_date')}")
                logger.debug(f"Album Genres: {album.get('genres')}")
                logger.debug(f"Album Label: {album.get('label')}")
                logger.debug(f"Album Popularity: {album.get('popularity')}")

                album_for_json = Album(
                    album.get('name'),
                    album_id,
                    album.get('album_type'),
                    album.get('release_date'),
                    album.get('genres'),
                    album.get('label'),
                    album.get('popularity')
                )

                albums_json.append(album_for_json)

                album_tracks_ids = []
                album_tracks = album.get('tracks').get('items')
                for track in album_tracks:
                    logger.info(f"Get Track {track.get('id')}")
                    logger.debug("")
                    logger.debug(f"Track Name: {track.get('name')}")
                    track_id = track.get('id')
                    logger.debug(f"Track ID: {track_id}")
                    album_tracks_ids.append(track_id)
                    logger.debug('Track Artists:')
                    track_artists = []
                    for track_artist in track.get('artists'):
                        track_artists.append(track_artist.get('id'))
                    logger.debug(track_artists)
                    logger.debug(f"Track Album ID: {[album_id]}")
                    logger.debug(f"Track Duration: {track.get('duration_ms')}")
                    logger.debug(f"Track Explicit: {track.get('explicit')}")

                    track_for_json = Track(
                        track.get('name'),
                        track_id,
                        track_artists,
                        [album_id],
                        track.get('duration_ms'),
                        track.get('explicit')
                    )
                    tracks_json.append(track_for_json)

                total_tracks_ids = len(album_tracks_ids)
                logger.info(f'Total tracks: {total_tracks_ids}')

                several_tracks_params = {
                    'ids': ''
                }

                track_id_offset = 50
                for j in range(0, total_tracks_ids, track_id_offset):
                    several_tracks_params['ids'] = (
                        ','.join(album_tracks_ids[j:j + track_id_offset])
                    )
                    # max 100 tracks = 2 requests per album
                    response = requests.get(
                        'https://api.spotify.com/v1/tracks',
                        params=several_tracks_params,
                        headers=headers,
                        timeout=10
                    )
                    time.sleep(timeout)
                    request_count += 1
                    logger.info(
                        f"[*] [Request {request_count} - {response.status_code}]")

                    if response.status_code != 200:
                        logger.warning('Token expired!')

                        response = requests.post(
                            'https://accounts.spotify.com/api/token',
                            data=token_data,
                            timeout=10
                        )
                        time.sleep(timeout)
                        request_count += 1
                        logger.info(
                            f"[*] [Request {request_count} - {response.status_code}]")

                        headers[
                            'Authorization'
                        ] = (
                            f"{response.json().get('token_type')}"
                            f"  {response.json().get('access_token')}"
                        )

                        response = requests.get(
                            'https://api.spotify.com/v1/tracks',
                            params=several_tracks_params,
                            headers=headers,
                            timeout=10
                        )
                        time.sleep(timeout)
                        request_count += 1
                        logger.info(
                            f"[*] [Request {request_count} - {response.status_code}]")

                    logger.info(f"Get tracks popularity")

                    tracks_data = response.json().get('tracks')
                    for track_obj in tracks_data:
                        logger.debug(f"Track ID: {track_obj.get('id')}")
                        logger.debug(f"Track Popularity: {track_obj.get('popularity')}")

                        for tracks_i in tracks_json:
                            if tracks_i.track_id == track_obj.get('id'):
                                tracks_i.popularity = track_obj.get('popularity')

                several_features_params = {
                    'ids': '',
                }

                track_features_offset = 100
                for k in range(0, total_tracks_ids, track_features_offset):
                    several_features_params['ids'] = (
                        ','.join(album_tracks_ids[k: k + track_features_offset])
                    )
                    # max 100 tracks = 1 request per album
                    response = requests.get(
                        'https://api.spotify.com/v1/audio-features',
                        params=several_features_params,
                        headers=headers,
                        timeout=10
                    )
                    time.sleep(timeout + 1)
                    request_count += 1
                    logger.info(
                        f"[*] [Request {request_count} - {response.status_code}]")

                    if response.status_code != 200:
                        logger.warning('Token expired!')

                        response = requests.post(
                            'https://accounts.spotify.com/api/token',
                            data=token_data,
                            timeout=10
                        )
                        time.sleep(timeout)
                        request_count += 1
                        logger.info(
                            f"[*] [Request {request_count} - {response.status_code}]")

                        headers[
                            'Authorization'
                        ] = (
                            f"{response.json().get('token_type')}"
                            f"  {response.json().get('access_token')}"
                        )

                        response = requests.get(
                            'https://api.spotify.com/v1/audio-features',
                            params=several_features_params,
                            headers=headers,
                            timeout=10
                        )
                        time.sleep(timeout)
                        request_count += 1
                        logger.info(
                            f"[*] [Request {request_count} - {response.status_code}]")

                    logger.info(f"Get tracks audio features")

                    features_data = response.json().get('audio_features')
                    for features_track in features_data:
                        try:
                            features_track.get('id')
                        except AttributeError:
                            logger.error('AttributeError')
                            continue

                        logger.info(f"Get Track {features_track.get('id')} features")
                        logger.debug(f"Track ID: {features_track.get('id')}")
                        logger.debug(f"Track Acousticness: {features_track.get('acousticness')}")
                        logger.debug(f"Track Danceability: {features_track.get('danceability')}")
                        logger.debug(f"Track Energy: {features_track.get('energy')}")
                        logger.debug(f"Track Instrumentalness: {features_track.get('instrumentalness')}")
                        logger.debug(f"Track Key: {features_track.get('key')}")
                        logger.debug(f"Track Liveness: {features_track.get('liveness')}")
                        logger.debug(f"Track Loudness: {features_track.get('loudness')}")
                        logger.debug(f"Track Mode: {features_track.get('mode')}")
                        logger.debug(f"Track Speechiness: {features_track.get('speechiness')}")
                        logger.debug(f"Track Tempo: {features_track.get('tempo')}")
                        logger.debug(f"Track Time signature: {features_track.get('time_signature')}")
                        logger.debug(f"Track Valence: {features_track.get('valence')}")

                        for tracks_j in tracks_json:
                            if tracks_j.track_id == features_track.get('id'):
                                tracks_j.acousticness = features_track.get('acousticness')
                                tracks_j.danceability = features_track.get('danceability')
                                tracks_j.energy = features_track.get('energy')
                                tracks_j.instrumentalness = features_track.get('instrumentalness')
                                tracks_j.key = features_track.get('key')
                                tracks_j.liveness = features_track.get('liveness')
                                tracks_j.loudness = features_track.get('loudness')
                                tracks_j.mode = features_track.get('mode')
                                tracks_j.speechiness = features_track.get('speechiness')
                                tracks_j.tempo = features_track.get('tempo')
                                tracks_j.time_signature = features_track.get('time_signature')
                                tracks_j.valence = features_track.get('valence')

        artist_for_json.albums = albums_json
        artist_for_json.tracks = tracks_json

        json_string = json.dumps(
            artist_for_json,
            indent=4,
            ensure_ascii=False,
            default=lambda x: x.__dict__
        )
        with open(
                f'src/aggregator/resources/artists/artist-{artist_id}.json',
                mode='w',
                encoding='utf-8'
        ) as file:
            file.write(json_string)

        logger.info(f"Get Artist {artist_id}")

        logger.info(f'[T] Time: {datetime.datetime.now()}')
