class City:

    TABLE_NAME = 'city'

    cache_by_id = {}
    cache_by_name = {}

    def __init__(self, id, name, country, region):
        self.id = id
        self.name = name
        self.country = country
        self.region = region

        City.cache_by_id.setdefault(id, (name, country, region))
        City.cache_by_name.setdefault(City._get_name_key(name, country, region), id)

    @staticmethod
    def _get_name_key(name, country, region):
        return '\t'.join((name, country, region))

    @staticmethod
    def get_id(conn, name, country, region):
        name_key = City._get_name_key(name, country, region)
        id = City.cache_by_name.get(name_key)
        if id != None:
            return id

        with conn.cursor() as cur:
            cur.execute(f'SELECT id FROM {City.TABLE_NAME} WHERE name = %s AND country = %s AND region = %s',
                (name, country, region))
            id = cur.fetchone()

        if id == None:
            try:
                with conn.cursor() as cur:
                    cur.execute(f'INSERT INTO {City.TABLE_NAME} (name, country, region) VALUES (%s, %s, %s) RETURNING id',
                        (name, country, region))
                    id = cur.fetchone()
            except Exception as e:
                print(e)
                return None

        id = id[0]

        City.cache_by_id[id] = (name, country, region)
        City.cache_by_name[name_key] = id

        return id

    @staticmethod
    def get_name(conn, id):
        name = City.cache_by_id.get(id)
        if name != None:
            return name

        with conn.cursor() as cur:
            cur.execute(f'SELECT name, country, region FROM {City.TABLE_NAME} WHERE id = %s', (id,))
            name = cur.fetchone()

        if name != None:
            City.cache_by_id[id] = name
            City.cache_by_name[City._get_name_key(*name)] = id

        return name


