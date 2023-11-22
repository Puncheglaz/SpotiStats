class Album:

    TABLE_NAME = 'album'

    def __init__(self, id, spotify_id, album_type_id, name, release_date, label, popularity):
        self.id = id
        self.spotify_id = spotify_id
        self.album_type_id = album_type_id
        self.name = name
        self.release_date = release_date
        self.label = label
        self.popularity = popularity

    @staticmethod
    def save(conn, spotify_id, album_type_id, name, release_date, label, popularity):
        try:
            with conn.cursor() as cur:
                cur.execute(f'''
                        INSERT INTO {Album.TABLE_NAME} (spotify_id, album_type_id, name, release_date, label, popularity)
                        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (spotify_id) DO UPDATE
                        SET (spotify_id, album_type_id, name, release_date, label, popularity) =
                            (EXCLUDED.spotify_id, EXCLUDED.album_type_id, EXCLUDED.name, EXCLUDED.release_date, EXCLUDED.label, EXCLUDED.popularity)
                    ''', spotify_id, album_type_id, name, release_date, label, popularity)
                return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_by_id(conn, id):
        if not id: return None

        with conn.cursor() as cur:
            cur.execute(f'''
                    SELECT spotify_id, album_type_id, name, release_date, label, popularity
                    FROM {Album.TABLE_NAME} WHERE id = %s
                ''', id)
            result = cur.fetchone()

        if not result: return None

        return Album(id, *result)