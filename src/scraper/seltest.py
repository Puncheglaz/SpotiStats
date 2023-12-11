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
# driver.get('')

# def setup():
#     driver.switch_to.window(driver.window_handles[0])

def get_net_data():
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
                data.append((resp_url, driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']))
            except Exception as e: print(e)
        # print(f"Caught {resp_url}")
        # print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body'])

    return data

def save_album_data(proc, start_time, save_cnt):
    for entry in get_net_data():
        if 'operationName=getAlbum&' in entry[0]:
            album_id = entry[0][entry[0].find('album%3A') + 8:]
            album_id = album_id[:album_id.find('%')]
            # if f'{album_id}.json' not in os.listdir('albums'):
            if album_id not in proc:
                with open(f'albums/{album_id}.json', 'w') as f:
                    f.write(entry[1])

                save_cnt += 1
                print(album_id, save_cnt, (time.time() - start_time)/save_cnt)

    return save_cnt

def parser():
    processed = set(x.split('.')[0] for x in os.listdir('albums'))

    start_time = time.time()
    save_cnt = 0

    i = 0
    for artist in os.listdir('artists'):
        i += 1
        print(i, artist)

        with open('artists/' + artist) as f:
            data = json.load(f)

        for album in data['albums']:
            if album['album_id'] not in processed:
                driver.get('https://open.spotify.com/album/' + album['album_id'])
                time.sleep(1)
                save_cnt = save_album_data(processed, start_time, save_cnt)

def main():
    input("\n\nSet up VPN & open spotify in the first tab\n\n[Press ENTER to continue]")

    attempts = 0

    while True:
        attempts += 1
        print(f'Atttempt #{attempts}')
        try:
            parser()
        except Exception as e:
            print(e)
        time.sleep(30)


main()