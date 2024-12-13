import entity.album
import entity.track
import entity.artist

def execute(conn, data):
    try:
        artist_id = entity.artist.Artist.save(conn,
                data['artist_id'],  # spotify_id
                data['name'],
                data.get('followers'),
                data.get('popularity'),
                data.get('monthly_listeners'),
                data.get('world_rank'),
                data.get('genres', []),
                data.get('top_cities', [])
            )

        if 'albums' in data:
            for album in data['albums']:
                entity.album.Album.save(conn,
                        album['album_id'],  # spotify_id
                        album['album_name'],
                        album.get('album_type'),
                        album.get('release_date'),
                        album.get('label'),
                        album.get('popularity'),
                        artist_id,
                        album.get('genres', [])
                    )

        if 'tracks' in data:
            for track in data['tracks']:
                entity.track.Track.save(conn,
                        track['track_id'],  # spotify_id
                        track['track_name'],
                        track.get('duration_ms'),
                        track.get('explicit'),
                        track.get('popularity'),
                        {
                            k: track.get(k) for k in [
                                "acousticness",
                                "danceability",
                                "energy",
                                "instrumentalness",
                                "key",
                                "liveness",
                                "loudness",
                                "mode",
                                "speechiness",
                                "tempo",
                                "time_signature",
                                "valence"
                            ]
                        },
                        track.get('plays'),
                        track.get('artists', []),
                        track.get('albums', []),
                    )

        conn.commit()


    except KeyError as e:
        return 'malformed json: no such key ' + str(e), 500

    return 'ok', 200
