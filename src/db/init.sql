CREATE TABLE genre (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(256)
);

CREATE TABLE city (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(256),
  country     VARCHAR(48),
  region      VARCHAR(48)
);

CREATE TABLE album_type (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(256)
);

CREATE TABLE artist (
  id          SERIAL PRIMARY KEY,
  spotify_id  VARCHAR(24) UNIQUE,
  name        VARCHAR(256),
  followers   BIGINT,
  popularity  SMALLINT,
  monthly_listeners BIGINT,
  world_rank  BIGINT
);

CREATE TABLE album (
  id          SERIAL PRIMARY KEY,
  spotify_id  VARCHAR(24) UNIQUE,
  name        VARCHAR(256),
  album_type_id SERIAL REFERENCES album_type(id),
  release_date DATE,
  label       VARCHAR(256),
  popularity  SMALLINT
);

CREATE TABLE track (
  id          SERIAL PRIMARY KEY,
  spotify_id  VARCHAR(24) UNIQUE,
  name        VARCHAR(512),
  duration_ms INTEGER,
  explicit    BOOLEAN,
  popularity  SMALLINT,
  features    JSONB,
  plays       BIGINT
);

CREATE TABLE album__artist (
  album_id    SERIAL REFERENCES album(id),
  artist_id   SERIAL REFERENCES artist(id),
  PRIMARY KEY(album_id, artist_id)
);

CREATE TABLE album__genre (
  album_id    SERIAL REFERENCES album(id),
  genre_id    SERIAL REFERENCES genre(id),
  PRIMARY KEY(album_id, genre_id)
);

CREATE TABLE album__track (
  album_id    SERIAL REFERENCES album(id),
  track_id    SERIAL REFERENCES track(id),
  PRIMARY KEY(album_id, track_id)
);

CREATE TABLE artist__city (
  artist_id   SERIAL REFERENCES artist(id),
  city_id     SERIAL REFERENCES city(id),
  monthly_plays BIGINT,
  PRIMARY KEY(artist_id, city_id)
);

CREATE TABLE artist__genre (
  artist_id   SERIAL REFERENCES artist(id),
  genre_id    SERIAL REFERENCES genre(id),
  PRIMARY KEY(artist_id, genre_id)
);

CREATE TABLE artist__track (
  artist_id   SERIAL REFERENCES artist(id),
  track_id    SERIAL REFERENCES track(id),
  PRIMARY KEY(artist_id, track_id)
);