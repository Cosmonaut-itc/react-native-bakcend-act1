import json

from flask import Flask, jsonify
import os
import psycopg2
from markupsafe import escape
import sys
from flask_cors import CORS

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='cosmo',
                            password='admin')
    return conn

CORS(app)

@app.route('/')
def default(): # put application's code here
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM songs;')
    songs = cur.fetchall()

    cur.close()

    song_dic = []
    for i in songs:
        current = {
            "id" : i[0],
            "name" : i[1],
            "author" : i[2]
        }
        song_dic.append(current)

    return jsonify(song_dic)

@app.route('/songDetails/<string:song_id>')
def RequestSongDetail(song_id):
    song_id = json.loads(song_id)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM songs WHERE id = %d' % song_id)
    song = cur.fetchall()

    song_dic = []
    for i in song:
        current = {
            "id": i[0],
            "name": i[1],
            "author": i[2]
        }
        song_dic.append(current)

    return jsonify(song_dic)

if __name__ == '__main__':
    app.run()
