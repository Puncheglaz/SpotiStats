import json
import requests
from auth_credentials import client_id, client_secret

token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}


def get_related_artists(artists_ids, headers, stage=0):
    artists_ids = list(set(artists_ids))
    total_artists = len(artists_ids)

    artists_ids_list = list()
    artists_ids_list.extend(artists_ids)
    process_num = 0
    for artist_id in artists_ids:
        process_num += 1
        print(f'Collect {process_num} of {total_artists}')
        response = requests.get(
            f'https://api.spotify.com/v1/artists/{artist_id}/related-artists',
            headers=headers
        )

        for artist in response.json().get('artists'):
            artists_ids_list.append(artist.get('id'))

    print(f'==============STAGE={stage}=============')
    print(f'       Total related artists: {len(artists_ids_list)}')
    print(f'Total unique related artists: {len(set(artists_ids_list))}')
    print(f'==================================')

    artists_ids_list = list(set(artists_ids_list))

    return artists_ids_list


def main():
    response = requests.post('https://accounts.spotify.com/api/token', data=token_data)

    access_token = response.json().get('access_token')
    token_type = response.json().get('token_type')

    headers = {
        'Authorization': f'{token_type}  {access_token}',
    }

    with open(f'src/aggregator/resources/spotify-followed-artists.json', 'r', encoding='utf-8') as file:
        artists_data = json.load(file)

    followed_artists_ids = list()
    for artist in artists_data.get('artists'):
        followed_artists_ids.append(artist.get('uri').split(':')[2])

    artists_ids_list_stage_one = get_related_artists(
        followed_artists_ids,
        headers=headers,
        stage=1
    )

    artists_ids_list = get_related_artists(
        artists_ids_list_stage_one,
        headers=headers,
        stage=2
    )

    json_string = json.dumps(
        artists_ids_list,
        indent=4,
        ensure_ascii=False
    )

    with open(f'src/aggregator/resources/artists-ids-list.json', 'w', encoding='utf-8') as file:
        file.write(json_string)


if __name__ == '__main__':
    main()
