import json
import pathlib
import sqlite3

def connect_db():
    try:
        with open('{}/.tempo/config.json'.format(pathlib.Path.home()), 'r') as cfg:
            config = json.load(cfg)
            conn = sqlite3.connect(config['db_path'])
            cursor = conn.cursor()
            cfg.close()
            return (conn, cursor)
    except Exception as err:
        print(err)
        exit(1)
