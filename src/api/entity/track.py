import json
from entity.artist import Artist
from entity.album import Album

class Track:

    TABLE_NAME = 'track'

    def __init__(self, id, spotify_id, name, duration_ms, explicit, popularity, features = {}, plays = None):
        self.id = id
        self.spotify_id = spotify_id
        self.name = name
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.popularity = popularity
        self.features = features
        self.plays = plays

    @staticmethod
    def save(conn, spotify_id, name, duration_ms, explicit, popularity, features = {}, plays = None, artists = [], albums = []):
        try:
            with conn.cursor() as cur:
                cur.execute(f'''
                        INSERT INTO {Track.TABLE_NAME} (spotify_id, name, duration_ms, explicit, popularity, features, plays)
                        VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (spotify_id) DO NOTHING RETURNING id
                    ''', (spotify_id, name, duration_ms, explicit, popularity, json.dumps(features), plays))
                id = cur.fetchone()

                if id == None:
                    cur.execute(f'SELECT id FROM {Track.TABLE_NAME} WHERE spotify_id = %s', (spotify_id,))
                    id = cur.fetchone()

                id = id[0]

                for artist in artists:
                    cur.execute(f'''
                            INSERT INTO {Artist.TABLE_NAME__TRACK} (artist_id, track_id)
                            SELECT id, %s FROM {Artist.TABLE_NAME} WHERE spotify_id = %s
                            ON CONFLICT (artist_id, track_id) DO NOTHING
                        ''', (id, artist))

                for album in albums:
                    cur.execute(f'''
                            INSERT INTO {Album.TABLE_NAME__TRACK} (album_id, track_id)
                            SELECT id, %s FROM {Album.TABLE_NAME} WHERE spotify_id = %s
                            ON CONFLICT (album_id, track_id) DO NOTHING
                        ''', (id, album))

                return id

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update(conn, spotify_id, popularity = None, features = None, plays = None):
        try:
            with conn.cursor() as cur:
                cur.execute(f'''
                        UPDATE {Track.TABLE_NAME} SET
                          popularity = COALESCE(%s, popularity),
                          features = COALESCE(%s, features),
                          plays = COALESCE(%s, plays)
                        WHERE spotify_id = %s
                    ''', (popularity, features, plays, spotify_id))
                return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_by_id(conn, id):
        if not id: return None

        with conn.cursor() as cur:
            cur.execute(f'''
                    SELECT spotify_id, name, duration_ms, explicit, popularity, features, plays
                    FROM {Track.TABLE_NAME} WHERE id = %s
                ''', (id,))
            result = cur.fetchone()

        if not result: return None

        return Track(id, *result)