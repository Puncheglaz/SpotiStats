from entity.genre import Genre
from entity.albumType import AlbumType

class Album:

    TABLE_NAME = 'album'
    TABLE_NAME__ARTIST = 'album__artist'
    TABLE_NAME__GENRE = 'album__genre'
    TABLE_NAME__TRACK = 'album__track'

    def __init__(self, id, spotify_id, album_type_id, name, release_date, label, popularity):
        self.id = id
        self.spotify_id = spotify_id
        self.album_type_id = album_type_id
        self.name = name
        self.release_date = release_date
        self.label = label
        self.popularity = popularity

    @staticmethod
    def save(conn, spotify_id, name, album_type, release_date, label, popularity, artist_id, genres = []):
        try:
            album_type_id = AlbumType.get_id(conn, album_type)

            with conn.cursor() as cur:
                cur.execute(f'''
                        INSERT INTO {Album.TABLE_NAME} (spotify_id, album_type_id, name, release_date, label, popularity)
                        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (spotify_id) DO NOTHING RETURNING id
                    ''', (spotify_id, album_type_id, name, release_date, label, popularity))

                id = cur.fetchone()

                if id == None:
                    cur.execute(f'SELECT id FROM {Album.TABLE_NAME} WHERE spotify_id = %s', (spotify_id,))
                    id = cur.fetchone()

                id = id[0]

                for genre in genres:
                    genre_id = Genre.get_id(conn, genre)
                    cur.execute(f'''
                            INSERT INTO {Album.TABLE_NAME__GENRE} (album_id, genre_id)
                            VALUES (%s, %s) ON CONFLICT (album_id, genre_id) DO NOTHING
                        ''', (id, genre_id))

                cur.execute(f'''
                        INSERT INTO {Album.TABLE_NAME__ARTIST} (album_id, artist_id)
                        VALUES (%s, %s) ON CONFLICT (album_id, artist_id) DO NOTHING
                    ''', (id, artist_id))

                return id

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_by_id(conn, id):
        if not id: return None

        with conn.cursor() as cur:
            cur.execute(f'''
                    SELECT spotify_id, album_type_id, name, release_date, label, popularity
                    FROM {Album.TABLE_NAME} WHERE id = %s
                ''', (id,))
            result = cur.fetchone()

        if not result: return None

        return Album(id, *result)