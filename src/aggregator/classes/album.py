"""Module for album class."""


class Album:
    """Class representing an album."""
    def __init__(self, album_name, album_id, album_type, release_date, genres, label, popularity):
        self.album_name = album_name
        self.album_id = album_id
        self.album_type = album_type
        self.release_date = release_date
        self.genres = genres
        self.label = label
        self.popularity = popularity

    def __str__(self):
        return f'{self.album_name} {self.album_id} {self.album_type}' \
               f' {self.release_date} {self.genres} {self.label} {self.popularity}'

    def get_album_name(self):
        """Function returns album_name."""
        return self.album_name
