import click
import sqlite3
import json

from collections import namedtuple
from datetime import date


Worklog = namedtuple('Worklog', ['description', 'time', 'issue', 'day'])
cursor = None
try:
    with open('config.json') as cfg:
        config = json.load(cfg)
        conn = sqlite3.connect(config['db_path'])
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS worklogs (
                            id integer PRIMARY KEY,
                            description text NOT NULL,
                            time integer NOT NULL,
                            issue text NOT NULL,
                            day text NOT NULL
                          );""")

        cfg.close()
except Error as err:
    if not cfg:
        print('Error: missing config.json file')
    else:
        print(err)
    exit(1)


@click.group()
def main():
    pass


@main.command()
@click.argument('description')
@click.argument('time')
@click.argument('issue')
@click.option('--day', '-d')
def work(description, time, issue, day=None):
    worklog = Worklog._make((description, time, issue, day or date.today().isoformat()))
    cursor.execute('INSERT INTO worklogs (description, time, issue, day) VALUES {}'.format(tuple(worklog)))


@main.command()
@click.argument('month')
def send_month(month):
    if 0 < month <= 12:
        pass
    else:
        print('Invalid month (1 to 12)')

@main.command()
@click.option('--month', '-m')
def ls(month):
    pass

if __name__ == '__main__':
    main()
