# from seleniumwire import webdriver
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import json
import os
import time

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument(r'user-data-dir=./User')
options.add_argument('--profile-directory=Profile1')

options.add_argument('--enable-logging')
options.add_argument('--log-level=0')
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

driver = webdriver.Chrome(chrome_options = options)

template_args = {
    'extension': None,
    'bearer': None,
    'client-token': None
}

def get_js_func(album_id):
    return f'''
    fetch("https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryArtistOverview&variables=%7B%22uri%22%3A%22spotify%3Aalbum%3A{album_id}%22%2C%22locale%22%3A%22%22%2C%22offset%22%3A0%2C%22limit%22%3A50%2C%22enableAssociatedVideos%22%3Afalse%7D&extensions={template_args['extension']}", {{
      "headers": {{
        "accept": "application/json",
        "accept-language": "en",
        "app-platform": "WebPlayer",
        "authorization": "{template_args['bearer']}",
        "client-token": "{template_args['client-token']}",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
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
    }});
    '''

def get_net_data():
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    def log_filter(log_):
        return (
            # is an actual response
            log_["method"] == "Network.requestWillBeSent"
            # and json
            # and "json" in log_["params"]["response"]["mimeType"]
        )

    data = []
    for log in filter(log_filter, logs):
        if 'operationName=queryArtistOverview&' in str(log):
            print(log)
        # request_id = log["params"]["requestId"]
        # resp_url = log["params"]["response"]["url"]

        # if 'operationName=getAlbum&' in resp_url:
        #     try:
        #         data.append((resp_url, driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']))
        #     except Exception as e: print(e)

def get_request_template():
    print('Getting request template...')
    driver.get_log("performance")
    driver.get('https://open.spotify.com/artist/4iHNK0tOyZPYnBU7nGAgpQ')
    time.sleep(3)

    for lr in driver.get_log("performance"):
        log = json.loads(lr["message"])["message"]
        if log["method"] == "Network.requestWillBeSent" and 'operationName=queryArtistOverview&' in log['params']['request']['url']:
            template_args['bearer'] = log['params']['request']['headers']['authorization']
            template_args['client-token'] = log['params']['request']['headers']['client-token']
            template_args['extension'] = log['params']['request']['url'].split('&')[-1][11:]
            print(template_args, '\n')
            break

def fetch_artist(artist_id):
    driver.get_log("performance")
    r = driver.execute_script(f'''
    await fetch("https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryArtistOverview&variables=%7B%22uri%22%3A%22spotify%3Aartist%3A{artist_id}%22%2C%22locale%22%3A%22%22%2C%22includePrerelease%22%3Atrue%7D&extensions={template_args['extension']}", {{
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
    }});
    ''')
    time.sleep(0.5)
    for lr in driver.get_log("performance"):
        log = json.loads(lr["message"])["message"]
        if log["method"] == "Network.responseReceived" and\
                'json' in log["params"]["response"]["mimeType"] and\
                'operationName=queryArtistOverview&' in log['params']['response']['url']:
            request_id = log["params"]["requestId"]
            try:
                return driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']
            except Exception as e: print(e)



def parser():
    get_request_template()

    processed = set(x.split('.')[0] for x in os.listdir('artist_stats'))

    start_time = time.time()
    save_cnt = 0
    prev_failed = False
    did_something = False

    i = 0
    for artist in sorted(os.listdir('artists')):
        i += 1
        print(i, artist)

        artist_id = artist.split('.')[0].split('-')[-1]

        if artist_id not in processed:
            d = fetch_artist(artist_id)

            if d == None:
                if prev_failed:
                    print('Two fails in a row, resetting session')
                    return did_something
                prev_failed = True
            else:
                with open(f'artist_stats/{artist_id}.json', 'w') as f:
                    f.write(d)

                did_something = True
                processed.add(artist_id)
                save_cnt += 1
                print(artist_id, save_cnt, (time.time() - start_time)/save_cnt)
    return did_something

def main():
    # input("\n\nSet up VPN & open spotify in the first tab\n\n[Press ENTER to continue]")

    attempts = 0

    while True:
        attempts += 1
        print(f'Atttempt #{attempts}')
        try:
            if not parser(): break
        except Exception as e:
            print(e)
        time.sleep(10)


main()
