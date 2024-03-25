import json

import pytest

from src.aggregator.auth_credentials import access_token, token_type


@pytest.fixture()
def get_headers():
    return {'Authorization': f'{token_type}  {access_token}'}


@pytest.fixture()
def get_artist_json_data():
    with open(
            file='tests/resources/artist-data.json',
            mode='r',
            encoding='utf-8'
    ) as file:
        data = json.load(file)
    return data
