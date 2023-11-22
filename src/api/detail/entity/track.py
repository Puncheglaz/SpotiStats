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
    def save(conn, spotify_id, name, duration_ms, explicit, popularity, features = {}, plays = None):
        try:
            with conn.cursor() as cur:
                cur.execute(f'''
                        INSERT INTO {Track.TABLE_NAME} (spotify_id, name, duration_ms, explicit, popularity, features, plays)
                        VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (spotify_id) DO NOTHING
                    ''', spotify_id, name, duration_ms, explicit, popularity, features, plays)
                return True
        except Exception as e:
            print(e)
            return False

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
                    ''', popularity, features, plays, spotify_id)
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
                ''', id)
            result = cur.fetchone()

        if not result: return None

        return Track(id, *result)