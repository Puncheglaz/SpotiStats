#!/bin/env python3

from flask import Flask, request
from flask_cors import CORS
import psycopg2
import traceback
import action.saveArtist
import action.getAverageFollowersPerGenres
import action.getTracksPerYearForGenre
import action.query
import config

app = Flask(__name__)
cors = CORS(app)

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

@app.route('/getAverageFollowersPerGenres', methods=['GET'])
@error_handler
def getAverageFollowersPerGenres():
    if request.method == 'GET':
        return action.getAverageFollowersPerGenres.execute(conn, None)

@app.route('/getTracksPerYearForGenre', methods=['GET'])
@error_handler
def getTracksPerYearForGenre():
    if request.method == 'GET':
        genre = request.args.get('genre')
        return action.getTracksPerYearForGenre.execute(conn, genre)

@app.route('/query', methods=['GET'])
@error_handler
def getQuery():
    if request.method == 'GET':
        return action.query.execute(conn, request.args)

if __name__ == '__main__':
    app.run(debug = True)

# conn.close()
print('finished')