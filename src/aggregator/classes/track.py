class Track:

    def __init__(self, track_name, track_id, artists, albums, duration_ms, explicit, popularity=None, acousticness=None,
                 danceability=None, energy=None, instrumentalness=None, key=None, liveness=None, loudness=None,
                 mode=None, speechiness=None, tempo=None, time_signature=None, valence=None):
        self.track_name = track_name
        self.track_id = track_id
        self.artists = artists
        self.albums = albums
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.popularity = popularity
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.key = key
        self.liveness = liveness
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.tempo = tempo
        self.time_signature = time_signature
        self.valence = valence

    def __str__(self):
        return f'{self.track_name} {self.track_id} {self.artists} {self.albums} {self.duration_ms} {self.explicit}' \
               f' {self.popularity} {self.acousticness} {self.danceability} {self.energy} {self.instrumentalness}' \
               f' {self.key} {self.liveness} {self.loudness} {self.mode} {self.speechiness} {self.tempo}' \
               f' {self.time_signature} {self.valence}'
