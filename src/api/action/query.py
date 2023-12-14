
def execute(conn, data):
    try:

        queryType = data.get('type')

        if queryType == 'tracksByYears':
            genre = data.get('genre')

            with conn.cursor() as cur:
                cur.execute(f'''
                        SELECT EXTRACT(YEAR FROM a.release_date) AS release_year, COUNT(DISTINCT t.id) AS track_count
                        FROM track t
                        JOIN album__track at ON t.id = at.track_id
                        JOIN album a ON a.id = at.album_id
                        JOIN album__artist aa ON a.id = aa.album_id
                        JOIN artist__genre ag ON aa.artist_id = ag.artist_id
                        JOIN genre g ON ag.genre_id = g.id
                        WHERE g."group" = %s OR g."name" = %s
                        GROUP BY release_year
                        ORDER BY release_year;
                    ''', (genre, genre))

                return cur.fetchall()

        elif queryType == 'playsByYears':
            genre = data.get('genre')

            with conn.cursor() as cur:
                cur.execute(f'''
                        SELECT EXTRACT(YEAR FROM a.release_date) AS release_year, SUM(t.plays) AS total_plays
                        FROM genre g
                        JOIN artist__genre ag ON g.id = ag.genre_id
                        JOIN artist__track art ON ag.artist_id = art.artist_id
                        JOIN track t ON art.track_id = t.id
                        JOIN album__track at ON t.id = at.track_id
                        JOIN album a ON at.album_id = a.id
                        WHERE g."group" = %s OR g."name" = %s
                        GROUP BY release_year
                        ORDER BY release_year;
                    ''', (genre, genre))

                return cur.fetchall()

        elif queryType == 'features':
            genre = data.get('genre')

            with conn.cursor() as cur:
                cur.execute(f'''
                        SELECT feature, AVG(value::numeric) AS avg_value
                        FROM track
                        JOIN artist__track ON track.id = artist__track.track_id
                        JOIN artist__genre ON artist__track.artist_id = artist__genre.artist_id
                        JOIN genre ON genre.id = artist__genre.genre_id
                        CROSS JOIN LATERAL jsonb_each_text(track.features) AS features(feature, value)
                        WHERE genre."group" = %s OR genre."name" = %s
                        GROUP BY feature
                        ORDER BY feature;
                    ''', (genre, genre))

                # return dict(cur.fetchall())
                return cur.fetchall()

        elif queryType == 'genresByPlays':

            with conn.cursor() as cur:
                cur.execute(f'''
                        SELECT genre_name,
                               SUM(plays) AS total_plays
                        FROM (
                            SELECT DISTINCT ON (t.id, g.id) plays,
                            CASE
                              WHEN g."group" IS NOT NULL THEN g."group"
                              ELSE g."name"
                            END  AS genre_name
                            FROM track t
                            JOIN artist__track at1 ON t.id = at1.track_id
                            JOIN artist__genre ag ON at1.artist_id = ag.artist_id
                            JOIN genre g ON ag.genre_id = g.id)
                        GROUP BY genre_name
                        ORDER BY total_plays DESC;
                    ''')

                return cur.fetchall()

        elif queryType == 'yearsByReleases':

            with conn.cursor() as cur:
                cur.execute(f'''
                        SELECT EXTRACT(YEAR FROM release_date) AS release_year,
                               SUM(plays) AS total_plays
                        FROM (
                        SELECT DISTINCT ON (t.id) plays, release_date
                          FROM album a
                               JOIN album__track at ON a.id = at.album_id
                               JOIN track t ON at.track_id = t.id)
                         GROUP BY release_year
                         ORDER BY total_plays DESC;
                    ''')

                return cur.fetchall()

        elif queryType == 'explicitByGenre':
            count = data.get('count', default = 5)

            with conn.cursor() as cur:
                cur.execute(f'''
                        SELECT
                          CASE
                            WHEN g."group" IS NOT NULL THEN g."group"
                            ELSE g."name"
                          END AS genre_name,
                          COUNT(t.id) AS explicit_track_count
                        FROM genre g
                        JOIN artist__genre ag ON g.id = ag.genre_id
                        JOIN artist__track at ON ag.artist_id = at.artist_id
                        JOIN track t ON at.track_id = t.id
                        WHERE t.explicit = TRUE
                        GROUP BY genre_name
                        ORDER BY COUNT(t.id) DESC LIMIT %s;
                    ''', (count, ))

                return cur.fetchall()

        elif queryType == 'topGenreAndArtistByCountries':

            with conn.cursor() as cur:
                cur.execute(f'''
                        WITH ranked_artists AS (
                          SELECT
                            ci.country,
                            ar.name AS artist_name,
                            ROW_NUMBER() OVER(PARTITION BY ci.country ORDER BY ac.monthly_plays DESC) AS rn
                          FROM artist__city ac
                          JOIN artist ar ON ac.artist_id = ar.id
                          JOIN city ci ON ac.city_id = ci.id
                        ),
                        ranked_genres AS (
                          SELECT
                            ci.country,
                            g.name AS genre_name,
                            ROW_NUMBER() OVER(PARTITION BY ci.country ORDER BY ac.monthly_plays DESC) AS rn
                          FROM artist__genre ag
                          JOIN genre g ON ag.genre_id = g.id
                          JOIN artist__city ac ON ag.artist_id = ac.artist_id
                          JOIN city ci ON ac.city_id = ci.id
                        )
                        SELECT 
                          ra.country AS country, 
                          ra.artist_name AS most_played_artist, 
                          rg.genre_name AS most_played_genre
                        FROM ranked_artists ra
                        JOIN ranked_genres rg ON ra.country = rg.country AND ra.rn = 1 AND rg.rn = 1;
                    ''')

                return cur.fetchall()

        elif queryType == 'genreByCountries':
            genre = data.get('genre')

            with conn.cursor() as cur:
                cur.execute(f'''
                        SELECT c.country, SUM(ac.monthly_plays) AS total_monthly_plays
                          FROM artist__genre ag
                               JOIN artist__city ac ON ag.artist_id = ac.artist_id
                               JOIN city c ON ac.city_id = c.id
                               JOIN artist__track at ON ag.artist_id = at.artist_id
                         WHERE ag.genre_id IN (SELECT id FROM genre WHERE "group" = %s OR "name" = %s)
                         GROUP BY c.country;
                    ''', (genre, genre))

                return cur.fetchall()

        elif queryType == 'genres':

            with conn.cursor() as cur:
                cur.execute('SELECT "name" FROM genre')

                return [x[0] for x in cur.fetchall()]

        else:
            return 'unknown'

    except KeyError as e:
        return 'malformed request: ' + str(e), 500

    return data, 200