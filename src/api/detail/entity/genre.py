class Genre:

    TABLE_NAME = 'genre'

    cache_by_id = {}
    cache_by_name = {}

    def __init__(self, id, name):
        self.id = id
        self.name = name

        Genre.cache_by_id.setdefault(id, name)
        Genre.cache_by_name.setdefault(name, id)

    @staticmethod
    def get_id(conn, name):
        id = Genre.cache_by_name.get(name)
        if id != None:
            return id

        with conn.cursor() as cur:
            cur.execute(f'SELECT id FROM {Genre.TABLE_NAME} WHERE name = %s', name)
            id = cur.fetchone()[0]

        if id == None:
            try:
                with conn.cursor() as cur:
                    cur.execute(f'INSERT INTO {Genre.TABLE_NAME} (name) VALUES (%s) RETURNING id', name)
                    id = cur.fetchone()[0]
            except Exception as e:
                print(e)
                return None

        Genre.cache_by_id[id] = name
        Genre.cache_by_name[name] = id

        return id

    @staticmethod
    def get_name(conn, id):
        name = Genre.cache_by_id.get(id)
        if name != None:
            return name

        with conn.cursor() as cur:
            cur.execute(f'SELECT name FROM {Genre.TABLE_NAME} WHERE id = %s', id)
            name = cur.fetchone()[0]

        if name != None:
            Genre.cache_by_id[id] = name
            Genre.cache_by_name[name] = id

        return name


