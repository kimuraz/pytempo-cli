import click
import time
import pathlib

from collections import namedtuple
from datetime import datetime, date, timedelta

from api import send_worklog
from db import connect_db
from config import set_config, set_db, get_config


Worklog = namedtuple('Worklog', ['id', 'description', 'time', 'issue', 'day'])


@click.group()
def main():
    pass


@main.command()
@click.option('--interactive', '-i', is_flag=True)
@click.option('--token', '-t')
@click.option('--account', '-a')
@click.option('--db', '-d')
def configure(interactive, token=None, account=None, db=None):
    cfg = None
    if interactive:
        cfg = {
            'token': click.prompt('Token'),
            'account_id': click.prompt('Account ID'),
            'db_path': click.prompt('Path to the DB', default='{}/.tempo/db.sqlite3'.format(pathlib.Path.home()))
        }
    else:
        if not token or not account or not db:
            print('Please, provide all the parameters (token, account id and db path) or enter the interactive mode -i')
            exit(1)
        cfg = {
            'token': token,
            'account_id': account,
            'db_path': db
        }
    set_config(cfg)
    set_db()


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
        (conn, cursor) = connect_db()
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
    (conn, cursor) = connect_db()
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
        (conn, cursor) = connect_db()
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
                args += "{}{}='{}'".format(',' if args else '',
                                           k, args_dict[k])
        if args:
            (conn, cursor) = connect_db()
            cursor.execute(
                'UPDATE worklogs SET {} WHERE id={}'.format(''.join(args), id))
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
    config = get_config()
    for w in worklogs:
        if send_worklog(w, config['token'], config['account_id']) and remove:
            ctx.invoke(rm, id=w.id)
        time.sleep(0.2)
