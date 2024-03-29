"""Module for artist class."""


class Artist:
    """Class representing an artist."""
    def __init__(self, artist_id, name, popularity, followers, genres, albums=None, tracks=None):
        self.artist_id = artist_id
        self.name = name
        self.popularity = popularity
        self.followers = followers
        self.genres = genres
        self.albums = albums
        self.tracks = tracks
        if type(name) is not str:
            raise TypeError("Artist name must be string.")

    def __str__(self):
        return f'{self.artist_id} {self.name} {self.popularity}' \
               f' {self.followers} {self.genres} {self.albums} {self.tracks}'

    def get_artist_name(self):
        """Function returns artist's name."""
        return self.name
