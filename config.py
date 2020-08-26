import json
import pathlib

from db import connect_db


def set_config(cfg):
    pathlib.Path(('{}/.tempo'.format(pathlib.Path.home()))
                 ).mkdir(parents=True, exist_ok=True)
    with open('{}/.tempo/config.json'.format(pathlib.Path.home()), 'w+') as f:
        f.write(json.dumps(cfg))
    f.close()


def set_db():
    (conn, cursor) = connect_db()
    cursor.execute("""CREATE TABLE IF NOT EXISTS worklogs (
                        id integer PRIMARY KEY,
                        description text NOT NULL,
                        time float NOT NULL,
                        issue text NOT NULL,
                        day date NOT NULL
                      );""")


def get_config():
    with open('{}/.tempo/config.json'.format(pathlib.Path.home()), 'r') as f:
        return json.load(f)
