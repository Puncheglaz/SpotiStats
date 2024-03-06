"""Module for fast selenium operations utils."""
import json
import os
import time

from selenium import webdriver

template_args = {
    'extension': None,
    'bearer': None,
    'client-token': None
}

FASTSEL_HEADERS = f'''{{
    "headers": {{
        "accept": "application/json",
        "accept-language": "en",
        "app-platform": "WebPlayer",
        "authorization": "{template_args['bearer']}",
        "client-token": "{template_args['client-token']}",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua": "\\"Chromium\\";v=\\"119\\", \\"Not?A_Brand\\";v=\\"24\\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\\"Linux\\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "spotify-app-version": "1.2.27.682.g02eef338"
    }},
    "referrer": "https://open.spotify.com/",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": null,
    "method": "GET",
    "mode": "cors",
    "credentials": "include"
}}'''


def setup_driver():
    """Function to prepare selenium webdriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(r'user-data-dir=./User')
    options.add_argument('--profile-directory=Profile1')

    options.add_argument('--enable-logging')
    options.add_argument('--log-level=0')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    web_driver = webdriver.Chrome(options=options)

    return web_driver


driver = setup_driver()


def get_request_template(request_mode, request_id, operation_name):
    """Function for getting request template."""
    print('Getting request template...')
    driver.get_log("performance")
    driver.get(f'https://open.spotify.com/{request_mode}/{request_id}')
    time.sleep(3)

    for log_rate in driver.get_log("performance"):
        log = json.loads(log_rate["message"])["message"]
        if log["method"] == "Network.requestWillBeSent" and \
                f'operationName={operation_name}&' in log['params']['request']['url']:
            template_args['bearer'] = log['params']['request']['headers']['authorization']
            template_args['client-token'] = log['params']['request']['headers']['client-token']
            template_args['extension'] = log['params']['request']['url'].split('&')[-1][11:]
            print(template_args, '\n')
            break


def fetch_object(request_mode, object_id, operation_name, request_options):
    """Function for object fetching by album_id."""
    driver.get_log("performance")
    driver.execute_script(
        """await fetch("https://api-partner.spotify.com/pathfinder/v1/query?""" +
        f"""operationName={operation_name}&variables=%7B%22uri%22%3A%22spotify%3A""" +
        f"""{request_mode}%3A{object_id}%22%2C%22locale%22%3A%22%22%2C%22""" +
        f"""{request_options}""" +
        f"""false%7D&extensions={template_args['extension']}", """ +
        FASTSEL_HEADERS +
        """);"""
    )
    time.sleep(0.5)
    for log_rate in driver.get_log("performance"):
        log = json.loads(log_rate["message"])["message"]
        if log["method"] == "Network.responseReceived" and \
                'json' in log["params"]["response"]["mimeType"] and \
                f'operationName={operation_name}&' in log['params']['response']['url']:
            request_id = log["params"]["requestId"]
            try:
                return driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": request_id}
                )['body']
            except ValueError as value_error:
                print(f'A Value Error exception occurred: {value_error}')
            except TypeError as type_error:
                print(f'A Type Error exception occurred: {type_error}')
    return None


def get_artist_data_from_file(artist):
    """Function for taking artist's data from file."""
    with open(
            'artists/' + artist,
            mode='r',
            encoding='utf-8'
    ) as file:
        data = json.load(file)
    return data


def parse_object(request_mode, request_id, operation_name, processed_file_name):
    """Function for object data parsing."""
    get_request_template(
        request_mode=request_mode,
        request_id=request_id,
        operation_name=operation_name
    )

    processed = set(x.split('.')[0] for x in os.listdir(f'{processed_file_name}'))

    start_time = time.time()
    save_cnt = 0
    prev_failed = False
    did_something = False

    i = 0
    for artist in sorted(os.listdir('artists')):
        i += 1
        print(i, artist)

        if request_mode == 'artist':
            artist_id = artist.split('.')[0].split('-')[-1]

            if artist_id not in processed:
                artist_data = fetch_object(
                    request_mode=request_mode,
                    object_id=artist_id,
                    operation_name=operation_name,
                    request_options='includePrerelease%22%3Atrue%7D&'
                )

                if artist_data is None:
                    if prev_failed:
                        print('Two fails in a row, resetting session')
                        return did_something
                    prev_failed = True
                else:
                    with open(
                            f'{processed_file_name}/{artist_id}.json',
                            mode='w',
                            encoding='utf-8'
                    ) as file:
                        file.write(artist_data)

                    did_something = True
                    processed.add(artist_id)
                    save_cnt += 1
                    print(artist_id, save_cnt, (time.time() - start_time) / save_cnt)
        elif request_mode == 'album':
            data = get_artist_data_from_file(artist)

            for album in data['albums']:
                if album['album_id'] not in processed:
                    album_data = fetch_object(
                        request_mode=request_mode,
                        object_id=album['album_id'],
                        operation_name=operation_name,
                        request_options=
                        'offset%22%3A0%2C%22' +
                        'limit%22%3A50%2C%22' +
                        'enableAssociatedVideos%22%3Afalse%7D&'
                    )

                    if album_data is None:
                        if prev_failed:
                            print('Two fails in a row, resetting session')
                            return did_something
                        prev_failed = True
                    else:
                        with open(
                                f'{processed_file_name}/{album["album_id"]}.json',
                                mode='w',
                                encoding='utf-8'
                        ) as file:
                            file.write(album_data)

                        did_something = True
                        processed.add(album["album_id"])
                        save_cnt += 1
                        print(album["album_id"], save_cnt, (time.time() - start_time) / save_cnt)
    return did_something


def get_net_data():
    """Function for getting network data and logging."""
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    def log_filter(log_):
        return (
            # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
        )

    data = []
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]

        if 'operationName=getAlbum&' in resp_url:
            try:
                data.append(
                    (resp_url, driver.execute_cdp_cmd(
                        "Network.getResponseBody",
                        {"requestId": request_id})['body']
                     )
                )
            except ValueError as value_error:
                print(f'A Value Error exception occurred: {value_error}')
            except TypeError as type_error:
                print(f'A Type Error exception occurred: {type_error}')

    return data


def save_album_data(proc, start_time, save_cnt):
    """Function for album data saving by processed albums (proc)."""
    for entry in get_net_data():
        if 'operationName=getAlbum&' in entry[0]:
            album_id = entry[0][entry[0].find('album%3A') + 8:]
            album_id = album_id[:album_id.find('%')]
            # if f'{album_id}.json' not in os.listdir('albums'):
            if album_id not in proc:
                with open(
                        f'albums/{album_id}.json',
                        mode='w',
                        encoding='utf-8'
                ) as file:
                    file.write(entry[1])

                save_cnt += 1
                print(album_id, save_cnt, (time.time() - start_time) / save_cnt)

    return save_cnt


def parser():
    """Function for album data parsing."""
    processed = set(x.split('.')[0] for x in os.listdir('albums'))

    start_time = time.time()
    save_cnt = 0

    i = 0
    for artist in sorted(os.listdir('artists')):
        i += 1
        print(i, artist)

        data = get_artist_data_from_file(artist)

        for album in data['albums']:
            if album['album_id'] not in processed:
                driver.get('https://open.spotify.com/album/' + album['album_id'])
                time.sleep(2)
                save_cnt = save_album_data(processed, start_time, save_cnt)


def data_scraping(
        request_mode='',
        request_id='',
        operation_name='',
        processed_file_name='',
        seltest_mode=False
):
    """Function for data scraping."""
    # input("\n\nSet up VPN & open spotify in the first tab\n\n[Press ENTER to continue]")

    attempts = 0

    while True:
        attempts += 1
        print(f'Atttempt #{attempts}')
        try:
            if seltest_mode:
                parser()
            else:
                if not parse_object(
                        request_mode=request_mode,
                        request_id=request_id,
                        operation_name=operation_name,
                        processed_file_name=processed_file_name
                ):
                    break
        except ValueError as value_error:
            print(f'A Value Error exception occurred: {value_error}')
        except TypeError as type_error:
            print(f'A Type Error exception occurred: {type_error}')
        time.sleep(10)
