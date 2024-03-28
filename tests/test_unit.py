import json
from os import listdir
from os.path import isfile, join

import pytest
import requests

from src.aggregator.artist_aggregate import get_related_artists, artist_aggregate_main
from src.aggregator.auth_credentials import access_token, token_type, client_headers
from src.aggregator.classes.album import Album
from src.aggregator.classes.artist import Artist
from src.aggregator.classes.track import Track
from src.aggregator.stats_from_files import stats_from_files_main
from src.aggregator.stats_update import stats_update_main
from src.aggregator.stats_utils import (
    get_artist_response_template, change_artist_data, change_track_data
)
from tests.util_classes import ResponseObject

params_for_get_related = (
    (
        ['00FQb4jTyendYWaN8pK0wa'],
        [{"artists": [{"id": "1"}, {"id": "2"}]}]
    ),
    (
        ['$2_.&+=-~()\\qS4*?!@#%^'],
        [{"artists": []}]
    ),
    (
        [''],
        [{"artists": []}]
    ),
    (
        [
            '00FQb4jTyendYWaN8pK0wa',
            '0M2HHtY3OOQzIZxrHkbJLT'
        ],
        [
            {"artists": [{"id": "1"}, {"id": "2"}]},
            {"artists": [{"id": "3"}, {"id": "4"}]},
        ]
    ),
)

get_related_ids = [
    (
        f'test_id: {par[0]}, '
        f'json_data-{params_for_get_related.index(par)}'
    ) for par in params_for_get_related
]


@pytest.mark.unit
@pytest.mark.parametrize(
    'test_ids, json_datas',
    params_for_get_related,
    ids=get_related_ids
)
def test_get_related_artists(requests_mock, test_ids, json_datas):
    """Test get_related_artists function with parameters test_ids as artists_ids
     with options of one positive id, negative id, empty id and two id."""
    for test_id in test_ids:
        requests_mock.get(
            url=f'https://api.spotify.com/v1/artists/{test_id}/related-artists',
            json=json_datas[test_ids.index(test_id)]
        )

    actual_ids_list = sorted(
        get_related_artists(
            test_ids,
            headers={}
        )
    )

    json_ids = [
        art_id.get('id') for json_data in json_datas
        for val in json_data.values() for art_id in val
    ]
    json_ids.extend(test_ids)

    expected_ids_list = sorted(json_ids)

    assert actual_ids_list == expected_ids_list


def mock_get_related_return(*args, **kwargs):
    """Mock function for the correct return values
     for the artist_aggregate_main test."""
    # prepare test data for test case 1
    with open(
            'tests/resources/followed-artists-test-0.json',
            mode='r',
            encoding='utf-8'
    ) as file:
        followed_test_one = json.load(file)

    followed_ids_one = []
    for artist in followed_test_one.get('artists'):
        followed_ids_one.append(artist.get('uri').split(':')[2])

    with open(
            'tests/resources/stage_one_ids-0.json',
            mode='r',
            encoding='utf-8'
    ) as stage_one_file:
        test_one_stage_one = json.load(stage_one_file)

    test_one_stage_one_ids = [artist for artist in test_one_stage_one]

    with open(
            'tests/resources/stage_two_ids-0.json',
            mode='r',
            encoding='utf-8'
    ) as stage_two_file:
        test_one_stage_two = json.load(stage_two_file)

    test_one_stage_two_ids = [artist for artist in test_one_stage_two]

    # prepare test data for test case 2
    with open(
            'tests/resources/followed-artists-test-1.json',
            mode='r',
            encoding='utf-8'
    ) as file:
        followed_test_two = json.load(file)

    followed_ids_two = []
    for artist in followed_test_two.get('artists'):
        followed_ids_two.append(artist.get('uri').split(':')[2])

    with open(
            'tests/resources/stage_one_ids-1.json',
            mode='r',
            encoding='utf-8'
    ) as stage_one_file:
        test_two_stage_one = json.load(stage_one_file)

    test_two_stage_one_ids = [artist for artist in test_two_stage_one]

    with open(
            'tests/resources/stage_two_ids-1.json',
            mode='r',
            encoding='utf-8'
    ) as stage_two_file:
        test_two_stage_two = json.load(stage_two_file)

    test_two_stage_two_ids = [artist for artist in test_two_stage_two]

    # mock function call args templates
    if args == (followed_ids_one,) and kwargs == {
        "headers": {
            'Authorization': f'{token_type}  {access_token}',
        },
        "stage": 1
    }:
        return test_one_stage_one_ids
    elif args == (test_one_stage_one_ids,) and kwargs == {
        "headers": {
            'Authorization': f'{token_type}  {access_token}',
        },
        "stage": 2
    }:
        return test_one_stage_two_ids
    elif args == (followed_ids_two,) and kwargs == {
        "headers": {
            'Authorization': f'{token_type}  {access_token}',
        },
        "stage": 1
    }:
        return test_two_stage_one_ids
    elif args == (test_two_stage_one_ids,) and kwargs == {
        "headers": {
            'Authorization': f'{token_type}  {access_token}',
        },
        "stage": 2
    }:
        return test_two_stage_two_ids
    elif args == ([],) and kwargs == {
        "headers": {
            'Authorization': f'{token_type}  {access_token}',
        },
        "stage": 1
    }:
        return []
    elif args == ([],) and kwargs == {
        "headers": {
            'Authorization': f'{token_type}  {access_token}',
        },
        "stage": 2
    }:
        return []


params_for_artist_aggregate = (
    (
        'tests/resources/followed-artists-test-0.json',
        'tests/resources/actual-artists-ids.json',
        'tests/resources/expected-artists-ids-0.json'
    ),
    (
        'tests/resources/followed-artists-test-1.json',
        'tests/resources/actual-artists-ids.json',
        'tests/resources/expected-artists-ids-1.json'
    ),
    (
        'tests/resources/followed-artists-test-2.json',
        'tests/resources/actual-artists-ids.json',
        'tests/resources/expected-artists-ids-2.json'
    )
)

artist_aggregate_main_ids = [
    (
        f'followed-artists-test-{params_for_artist_aggregate.index(par)}.json, '
        f'actual-artists-ids.json, '
        f'expected-artists-ids-{params_for_artist_aggregate.index(par)}.json'
    ) for par in params_for_artist_aggregate
]


@pytest.mark.unit
@pytest.mark.parametrize(
    'source_file_path, id_file_path, expected_file_path',
    params_for_artist_aggregate,
    ids=artist_aggregate_main_ids
)
def test_artist_aggregate_main(
        mocker, source_file_path, id_file_path, expected_file_path):
    """Test execution of artist_aggregate_main function
     to collect related artists from source_file_path file
    with two id, one id and empty id."""
    mocker.patch(
        'src.aggregator.artist_aggregate.get_related_artists',
        new=mock_get_related_return
    )
    artist_aggregate_main(
        source_file_path=source_file_path,
        id_file_path=id_file_path
    )

    with open(
            expected_file_path,
            mode='r',
            encoding='utf-8'
    ) as file:
        expected_ids_data = json.load(file)

    with open(
            id_file_path,
            mode='r',
            encoding='utf-8'
    ) as file:
        actual_ids_data = json.load(file)

    assert sorted(expected_ids_data) == sorted(actual_ids_data)


@pytest.mark.unit
def test_artist_aggregate_main_raises_exception():
    """Test of exception call by artist_aggregate_main function
     when collecting related artists from invalid source_file_path file."""
    with pytest.raises(json.decoder.JSONDecodeError) as excinfo:
        artist_aggregate_main(
            source_file_path='tests/resources/followed-artists-test-3.json',
            id_file_path='actual-artists-ids.json'
        )
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Expecting value: line 1 column 1 (char 0)'


params_for_album_class = (
    ("Come! See!!", "4UYc1NrDWoMpPV68It9Obh", "album", "2022-05-18", [], "M.O.O.N. Holdings", 24),
    ("", "", "", "", [], "", 0)
)

album_class_ids = [
    f'test-{params_for_album_class.index(par)}'
    for par in params_for_album_class
]


@pytest.mark.unit
@pytest.mark.parametrize(
    'album_name, album_id, album_type, release_date, genres, label, popularity',
    params_for_album_class,
    ids=album_class_ids
)
def test_album_class_methods(
        album_name, album_id, album_type, release_date, genres, label, popularity):
    """Test the Album class methods __init__, __str__, and get_album_name
     with positive and empty names."""
    test_album = Album(
        album_name=album_name,
        album_id=album_id,
        album_type=album_type,
        release_date=release_date,
        genres=genres,
        label=label,
        popularity=popularity
    )

    assert test_album.get_album_name() == album_name
    assert test_album.__str__() == f'{album_name} {album_id} {album_type}' \
                                   f' {release_date} {genres} {label} {popularity}'


@pytest.mark.unit
def test_album_class_exception():
    """Test the Album class method __init__ with negative names
     and check raising type exception."""
    with pytest.raises(TypeError) as excinfo:
        test_album = Album(
            album_name=32987,
            album_id="",
            album_type="albums",
            release_date="2022",
            genres=[],
            label="",
            popularity=0
        )
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Album name must be string.'


params_for_artist_class = (
    (
        "0M2HHtY3OOQzIZxrHkbJLT", "M|O|O|N", 44, 129917, ["synthwave"],
        [
            {
                "album_name": "Come! See!!",
                "album_id": "4UYc1NrDWoMpPV68It9Obh",
                "album_type": "album",
                "release_date": "2022-05-18",
                "genres": [],
                "label": "M.O.O.N. Holdings",
                "popularity": 24
            }
        ],
        [
            {
                "track_name": "Kintsugi",
                "track_id": "5OILFfuKykbUDiFKJRXP5w"
            }
        ]
    ),
    ("", "", 0, 0, [], [], [])
)

artist_class_ids = [
    f'test-{params_for_artist_class.index(params)}, '
    f'name-{params[1]}'
    for params in params_for_artist_class
]


@pytest.mark.unit
@pytest.mark.parametrize(
    'artist_id, name, popularity, followers, genres, albums, tracks',
    params_for_artist_class,
    ids=artist_class_ids
)
def test_artist_class_methods(
        artist_id, name, popularity, followers, genres, albums, tracks):
    """Test the Artist class methods __init__, __str__, and get_artist_name
     with positive and empty names."""
    test_artist = Artist(
        artist_id=artist_id,
        name=name,
        popularity=popularity,
        followers=followers,
        genres=genres,
        albums=albums,
        tracks=tracks
    )

    assert test_artist.get_artist_name() == name
    assert test_artist.__str__() == f'{artist_id} {name} {popularity}' \
                                    f' {followers} {genres} {albums} {tracks}'


@pytest.mark.unit
def test_artist_class_exception():
    """Test the Artist class method __init__ with negative names
     and check raising type exception."""
    with pytest.raises(TypeError) as excinfo:
        test_artist = Artist(
            artist_id="12345",
            name=87326,
            popularity=0,
            followers=0,
            genres=[],
            albums=[],
            tracks=[]
        )
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Artist name must be string.'


params_for_track_class = (
    (
        "Kintsugi", "5OILFfuKykbUDiFKJRXP5w",
        ["0M2HHtY3OOQzIZxrHkbJLT"], ["4UYc1NrDWoMpPV68It9Obh"],
        246323, "false", 20, 0.00949
    ),
    ("", "", [], [], 0, "", 0, 0.0)
)

track_class_ids = [
    f'test-{params_for_track_class.index(params)}, '
    f'track_name-{params[0]}'
    for params in params_for_track_class
]


@pytest.mark.unit
@pytest.mark.parametrize(
    'track_name, track_id, artists, albums, duration_ms, explicit, popularity, acousticness',
    params_for_track_class,
    ids=track_class_ids
)
def test_track_class_methods(
        track_name, track_id, artists, albums, duration_ms, explicit,
        popularity, acousticness):
    """Test the Track class methods __init__, __str__, and get_artist_name
     with positive and empty names."""
    test_track = Track(
        track_name=track_name,
        track_id=track_id,
        artists=artists,
        albums=albums,
        duration_ms=duration_ms,
        explicit=explicit,
        popularity=popularity,
        acousticness=acousticness
    )

    assert test_track.get_track_name() == track_name
    assert test_track.__str__() == f'{track_name} {track_id} {artists} {albums}' \
                                   f' {duration_ms} {explicit} {popularity}' \
                                   f' {acousticness}' + ' None' * 11


@pytest.mark.unit
def test_track_class_exception():
    """Test the Track class method __init__ with negative names
     and check raising type exception."""
    with pytest.raises(TypeError) as excinfo:
        test_track = Track(
            track_name=12345,
            track_id="",
            artists=[],
            albums=[],
            duration_ms=0,
            explicit="",
            popularity=0,
            acousticness=0.0
        )
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Track name must be string.'


params_for_get_template = (
    ("0M2HHtY3OOQzIZxrHkbJLT", 0), ("$2_.&+=-~()\\qS4*?!@#%^", 1),
    ("", 0), ("", 1)
)


@pytest.mark.unit
@pytest.mark.parametrize(
    'artist_id, request_count', params_for_get_template)
def test_get_artist_template(
        requests_mock, get_artist_json_data, artist_id, request_count):
    """Test get_artist_response_template function with parameters artist_id
     and request_count with options of one positive id, negative id,
     empty id and empty id increased count."""
    requests_mock.get(
        url='https://api-partner.spotify.com/pathfinder/v1/query',
        headers=client_headers,
        json=get_artist_json_data
    )

    count_before = request_count
    response, request_count = get_artist_response_template(
        artist_id=artist_id,
        timeout=0,
        request_count=request_count
    )

    assert response.json() == get_artist_json_data
    assert request_count == count_before + 1


@pytest.mark.unit
@pytest.mark.parametrize('artist_id', ['0M2HHtY3OOQzIZxrHkbJLT', '00FQb4jTyendYWaN8pK0wa'])
def test_change_artist_data(requests_mock, get_artist_json_data, artist_id):
    """Test change_artist_data function with artist_id parameter of two positive ids."""
    requests_mock.get(url='https://localhost:8080', json=get_artist_json_data)
    response = requests.get(url='https://localhost:8080')
    actual_ids = change_artist_data(
        response=response,
        artist_id=artist_id,
        file_path="tests/resources/artists"
    )

    with open(
            file=f'tests/resources/artists/artist-{artist_id}.json',
            mode='r',
            encoding='utf-8'
    ) as actual_file:
        actual_data = json.load(actual_file)

    expected_data = get_artist_json_data.get('data').get('artistUnion').get('stats')

    assert actual_data.get('followers') == expected_data.get('followers')
    assert actual_data.get('monthly_listeners') == expected_data.get('monthlyListeners')
    assert actual_data.get('world_rank') == expected_data.get('worldRank')
    assert actual_data.get('top_cities') == expected_data.get('topCities').get('items')

    expected_ids = []
    for album in actual_data.get('albums'):
        expected_ids.append(album.get('album_id'))

    assert actual_ids == expected_ids


@pytest.mark.unit
def test_change_artist_data_invalid_exception(requests_mock, get_artist_json_data):
    """Test change_artist_data function with artist_id parameter of invalid id."""
    requests_mock.get(url='https://localhost', json=get_artist_json_data)
    response = requests.get(url='https://localhost')
    with pytest.raises(json.JSONDecodeError) as excinfo:
        change_artist_data(
            response=response,
            artist_id="2kK21234",
            file_path="tests/resources"
        )
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Expecting value: line 1 column 1 (char 0)'


@pytest.mark.unit
def test_change_artist_data_empty_exception(requests_mock, get_artist_json_data):
    """Test change_artist_data function with artist_id parameter of empty id."""
    requests_mock.get(url='https://localhost:3030', json=get_artist_json_data)
    response = requests.get(url='https://localhost:3030')
    with pytest.raises(FileNotFoundError) as excinfo:
        change_artist_data(
            response=response,
            artist_id="",
            file_path="tests/resources"
        )
    exception_msg = excinfo.value.args[1]
    assert exception_msg == 'No such file or directory'


@pytest.mark.unit
@pytest.mark.parametrize('artist_id', ['0M2HHtY3OOQzIZxrHkbJLT'])
def test_change_track_data(get_tracks_json_data, artist_id):
    """Test change_track_data function with artist_id parameter of one positive id."""
    tracks_data = get_tracks_json_data.get('data').get('albumUnion').get('tracks').get('items')
    change_track_data(
        tracks_data=tracks_data,
        artist_id=artist_id,
        file_path='tests/resources/artists'
    )

    with open(
            file=f'tests/resources/artists/artist-{artist_id}.json',
            mode='r',
            encoding='utf-8'
    ) as actual_file:
        actual_data = json.load(actual_file).get('tracks')

    expected_data = get_tracks_json_data.get('data').get('albumUnion').get('tracks').get('items')

    for act_track in actual_data:
        for exp_track in expected_data:
            if act_track.get('track_id') == exp_track.get('track').get('uri').split(':')[2]:
                assert act_track.get('playcount') == exp_track.get('track').get('playcount')


@pytest.mark.unit
def test_change_track_data_invalid_exception(get_tracks_json_data):
    """Test change_track_data function with artist_id parameter of invalid id."""
    tracks_data = get_tracks_json_data.get('data').get('albumUnion').get('tracks').get('items')
    with pytest.raises(json.JSONDecodeError) as excinfo:
        change_track_data(
            tracks_data=tracks_data,
            artist_id="2kK21234",
            file_path="tests/resources"
        )
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Expecting value: line 1 column 1 (char 0)'


@pytest.mark.unit
def test_change_track_data_empty_exception(get_tracks_json_data):
    """Test change_track_data function with artist_id parameter of empty id."""
    tracks_data = get_tracks_json_data.get('data').get('albumUnion').get('tracks').get('items')
    with pytest.raises(FileNotFoundError) as excinfo:
        change_track_data(
            tracks_data=tracks_data,
            artist_id="",
            file_path="tests/resources"
        )
    exception_msg = excinfo.value.args[1]
    assert exception_msg == 'No such file or directory'


def get_mock_artist_data():
    """Function for returning artist data sample."""
    with open(
            file='tests/resources/artist-data.json',
            mode='r',
            encoding='utf-8'
    ) as file:
        data = json.load(file)
    return data


def mock_get_response_template(*args, **kwargs):
    """Mock function for get_artist_response_template
     with args and kwargs parameters."""
    response = ResponseObject(get_mock_artist_data(), 200)
    current_count = kwargs.get('request_count') + 1
    return response, current_count


@pytest.mark.unit
def test_stats_update_main(
        mocker, requests_mock, get_tracks_json_data, get_artist_json_data
):
    """Test stats_update_main function with artist_id parameter of one positive id."""
    artist_id = '0M2HHtY3OOQzIZxrHkbJLT'

    mocker.patch(
        'src.aggregator.stats_update.get_artist_response_template',
        side_effect=mock_get_response_template
    )

    requests_mock.get(
        url='https://api-partner.spotify.com/pathfinder/v1/query',
        headers=client_headers,
        json=get_tracks_json_data
    )

    stats_update_main(
        artist_ids=[artist_id],
        timeout=0,
        request_count=0,
        file_path='tests/resources/artists'
    )

    with open(
            file=f'tests/resources/artists/artist-{artist_id}.json'
    ) as actual_file:
        actual_data = json.load(actual_file)

    expected_artist_data = get_artist_json_data.get('data').get('artistUnion')

    assert actual_data.get('followers') == expected_artist_data.get('stats').get('followers')
    assert actual_data.get('monthly_listeners') == expected_artist_data.get('stats').get('monthlyListeners')
    assert actual_data.get('world_rank') == expected_artist_data.get('stats').get('worldRank')
    assert actual_data.get('top_cities') == expected_artist_data.get('stats').get('topCities').get('items')

    expected_tracks_data = get_tracks_json_data.get('data').get('albumUnion').get('tracks').get('items')

    for act_track in actual_data.get('tracks'):
        for exp_track in expected_tracks_data:
            if act_track.get('track_id') == exp_track.get('track').get('uri').split(':')[2]:
                assert act_track.get('playcount') == exp_track.get('track').get('playcount')


@pytest.mark.unit
def test_stats_update_main_invalid_exception(
        mocker, requests_mock, get_tracks_json_data, get_artist_json_data
):
    """Test stats_update_main function with artist_id parameter of invalid id."""
    artist_id = '2kK21234'

    mocker.patch(
        'src.aggregator.stats_update.get_artist_response_template',
        side_effect=mock_get_response_template
    )

    requests_mock.get(
        url='https://api-partner.spotify.com/pathfinder/v1/query',
        headers=client_headers,
        json=get_tracks_json_data
    )

    with pytest.raises(json.JSONDecodeError) as excinfo:
        stats_update_main(
            artist_ids=[artist_id],
            timeout=0,
            request_count=0,
            file_path='tests/resources'
        )
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Expecting value: line 1 column 1 (char 0)'


@pytest.mark.unit
def test_stats_update_main_empty_exception(
        mocker, requests_mock, get_tracks_json_data, get_artist_json_data
):
    """Test stats_update_main function with artist_id parameter of empty id."""
    artist_id = ''

    mocker.patch(
        'src.aggregator.stats_update.get_artist_response_template',
        side_effect=mock_get_response_template
    )

    requests_mock.get(
        url='https://api-partner.spotify.com/pathfinder/v1/query',
        headers=client_headers,
        json=get_tracks_json_data
    )

    with pytest.raises(FileNotFoundError) as excinfo:
        stats_update_main(
            artist_ids=[artist_id],
            timeout=0,
            request_count=0,
            file_path='tests/resources'
        )
    exception_msg = excinfo.value.args[1]
    assert exception_msg == 'No such file or directory'


@pytest.mark.unit
def test_stats_from_files_main(
        mocker, get_tracks_json_data, get_artist_json_data
):
    """Test stats_from_files_main function with positive artist ids."""
    mocker.patch(
        'src.aggregator.stats_from_files.get_artist_response_template',
        side_effect=mock_get_response_template
    )

    stats_from_files_main(
        artists_path="tests/resources/artists",
        timeout=1,
        request_count=0,
        file_path="tests/resources/artists",
        artist_count=0,
        albums_path="tests/resources/albums"
    )

    artists_files_list = listdir("tests/resources/artists")
    # artists_files_list.remove('.DS_Store')
    artist_ids = [
        file.split('.')[0].split('-')[1] for file in artists_files_list if isfile(
            join(
                "tests/resources/artists",
                file
            )
        )
    ]

    for artist_id in artist_ids:
        with open(
                file=f'tests/resources/artists/artist-{artist_id}.json'
        ) as actual_file:
            actual_data = json.load(actual_file)

        expected_artist_data = get_artist_json_data.get('data').get('artistUnion')

        assert actual_data.get('followers') == expected_artist_data.get('stats').get('followers')
        assert actual_data.get('monthly_listeners') == expected_artist_data.get('stats').get('monthlyListeners')
        assert actual_data.get('world_rank') == expected_artist_data.get('stats').get('worldRank')
        assert actual_data.get('top_cities') == expected_artist_data.get('stats').get('topCities').get('items')

        expected_tracks_data = get_tracks_json_data.get('data').get('albumUnion').get('tracks').get('items')

        for act_track in actual_data.get('tracks'):
            for exp_track in expected_tracks_data:
                if act_track.get('track_id') == exp_track.get('track').get('uri').split(':')[2]:
                    assert act_track.get('playcount') == exp_track.get('track').get('playcount')


@pytest.mark.unit
def test_stats_from_files_main_invalid_exception(
        mocker, get_tracks_json_data, get_artist_json_data
):
    """Test stats_from_files_main function with invalid artist ids."""
    mocker.patch(
        'src.aggregator.stats_from_files.get_artist_response_template',
        side_effect=mock_get_response_template
    )

    with pytest.raises(json.JSONDecodeError) as excinfo:
        stats_from_files_main(
            artists_path="tests/resources/artist-test",
            timeout=1,
            request_count=0,
            file_path="tests/resources/artist-test",
            artist_count=0,
            albums_path="tests/resources/album-test"
        )
    exception_msg = excinfo.value.args[0]
    print(exception_msg)
    assert exception_msg == 'Expecting value: line 1 column 1 (char 0)'


@pytest.mark.unit
def test_stats_from_files_main_empty_exception(
        mocker, get_tracks_json_data, get_artist_json_data
):
    """Test stats_from_files_main function with empty artist ids."""
    mocker.patch(
        'src.aggregator.stats_from_files.get_artist_response_template',
        side_effect=mock_get_response_template
    )

    with pytest.raises(FileNotFoundError) as excinfo:
        stats_from_files_main(
            artists_path="tests/resources/artist",
            timeout=1,
            request_count=0,
            file_path="tests/resources/artist",
            artist_count=0,
            albums_path="tests/resources/album"
        )
    exception_msg = excinfo.value.args[1]
    assert exception_msg == 'No such file or directory'
