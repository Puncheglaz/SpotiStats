#!/bin/env python3

from flask import Flask, request
import psycopg2
import traceback
import action.saveArtist
import config

app = Flask(__name__)

conn = psycopg2.connect(
        host = config.DB_HOST,
        port = config.DB_PORT,
        dbname = config.DB_NAME,
        user = config.DB_USER,
        password = config.DB_PASS
    )

def error_handler(func):
    def Inner_Function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # print(e)
            traceback.print_exc()
            return 'error', 500
    Inner_Function.__name__ = func.__name__
    return Inner_Function

@app.route('/saveArtist', methods=['POST'])
@error_handler
def saveArtist():
    if request.method == 'POST':
        data = request.get_json()
        return action.saveArtist.execute(conn, data)

if __name__ == '__main__':
    app.run(debug = True)

# conn.close()
print('finished')