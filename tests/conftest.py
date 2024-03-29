import json

import pytest


@pytest.fixture()
def get_artist_json_data():
    with open(
            file='tests/resources/artist-data.json',
            mode='r',
            encoding='utf-8'
    ) as file:
        data = json.load(file)
    return data


@pytest.fixture()
def get_tracks_json_data():
    with open(
            file='tests/resources/tracks-data.json',
            mode='r',
            encoding='utf-8'
    ) as file:
        data = json.load(file)
    return data
