#!/usr/bin/env python3
import click
import sqlite3
import json

from collections import namedtuple
from datetime import datetime, date, timedelta 


Worklog = namedtuple('Worklog', ['description', 'time', 'issue', 'day'])
conn = None
cursor = None
try:
    with open('config.json') as cfg:
        config = json.load(cfg)
        conn = sqlite3.connect(config['db_path'])
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS worklogs (
                            id integer PRIMARY KEY,
                            description text NOT NULL,
                            time float NOT NULL,
                            issue text NOT NULL,
                            day date NOT NULL
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
    try:
        worklog = Worklog._make((description, time, issue, datetime.strptime(day, '%d-%m-%y') if day else date.today().isoformat()))
        cursor.execute('INSERT INTO worklogs (description, time, issue, day) VALUES {};'.format(tuple(worklog)))
        conn.commit()
    except Error as e:
        print(e)


@main.command()
@click.argument('month')
def send_month(month):
    if 0 < month <= 12:
        pass
    else:
        print('Invalid month (1 to 12)')

@main.command()
@click.option('--month', '-m')
@click.option('--today', '-t')
def ls(month, today):
    q = 'SELECT * FROM worklogs'
    if month:
        d = date(date.today().year, int(month), 1)
        q = '{} WHERE day BETWEEN {} AND {}'.format(q, d, date(d.year, d.month+1, d.day) - timedelta(1))
    q += ';'
    print(q)
    cursor.execute(q)
    rows = cursor.fetchall()
    print(rows)

if __name__ == '__main__':
    main()
