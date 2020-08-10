#!/usr/bin/env python3
import click
import json
import sqlite3

from collections import namedtuple
from datetime import datetime, date, timedelta


Worklog = namedtuple('Worklog', ['id', 'description', 'time', 'issue', 'day'])
conn = None
cursor = None
config = None
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
except Exception as err:
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
def work(description, time, issue, day):
    """
    Add a new worklog to the database
    """
    try:
        d = datetime.strptime(day, '%d-%m-%Y').date() if day else date.today()
        worklog = Worklog._make(
            (None, description, time, issue, d.isoformat()))
        cursor.execute('INSERT INTO worklogs (description, time, issue, day) VALUES {};'.format(
            tuple(worklog[1:])))
        conn.commit()
    except Exception as e:
        print(e)


@main.command()
@click.option('--month', '-m')
@click.option('--today', '-t', is_flag=True)
def ls(month, today, stdout=True):
    """
    Lists database worklogs
    """
    q = 'SELECT * FROM worklogs'
    worklogs = []
    total_hours = 0

    if month:
        d = date(date.today().year, int(month), 1)
        q = "{} WHERE day BETWEEN '{}' AND '{}'".format(
            q, d, date(d.year, d.month+1, d.day) - timedelta(1))
    elif today:
        q = "{} WHERE day='{}'".format(q, date.today().isoformat())

    q += ' ORDER BY day ASC;'
    cursor.execute(q)
    rows = cursor.fetchall()

    if len(rows):
        worklogs = [Worklog._make(row) for row in rows]
        total_hours = sum([w.time for w in worklogs])

    if stdout:
        print('\n'.join([str(w) for w in worklogs]))
        print('TOTAL HOURS: {}'.format(total_hours))
    
    return worklogs


@main.command()
@click.argument('id')
def rm(id):
    """
    Removes a worklog from the database
    """
    try:
        cursor.execute('DELETE FROM worklogs WHERE id={}'.format(id))
        conn.commit()
    except Exception as e:
        print(e)

@main.command()
@click.argument('id')
@click.option('--date', '-d')
@click.option('--description')
@click.option('--time', '-t')
@click.option('--issue', '-i')
def edit(id, date, description, time, issue):
    try:
        args_dict = locals()
        args = ''
        for k in args_dict.keys():
            if args_dict[k] and k != 'id':
                args += "{}{}='{}'".format(',' if args else '', k, args_dict[k])
        if args:
            cursor.execute('UPDATE worklogs SET {} WHERE id={}'.format(''.join(args),id))
            conn.commit()
    except Exception as e:
        print(e)


@main.command()
@click.option('--today', '-t', is_flag=True)
@click.option('--month', '-m')
@click.option('--remove', '-rm', is_flag=True)
@click.pass_context
def send(ctx, today, month, remove):
    """
    Send worklogs to tempo through REST requests.
    """
    worklogs = ctx.invoke(ls, month=month, today=today, stdout=False) 


if __name__ == '__main__':
    main()
