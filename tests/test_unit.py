import json

import pytest

from src.aggregator.artist_aggregate import get_related_artists, artist_aggregate_main
from src.aggregator.auth_credentials import access_token, token_type

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
