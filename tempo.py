import datetime
import click
import sqlite3
import json

from collections import namedtuple


Worklog = namedtuple('Worklog', ['description', 'time', 'issue', 'day'])
cursor = None

@click.group()
def main():
    try:
        with open('config.json') as cfg:
            config = json.load(cfg)
            conn = sqlite3.connect(config['db_path'])

            cfg.close()
    except:
        print('Error: missing config.json file')
        exit(1)
    pass

@main.command()
@click.argument('description')
@click.argument('time')
@click.argument('issue')
@click.argument('day')
@click.option('--repeat', '-r')
def work(description, time, issue, day, repeat = False):
    if repeat:
        pass
    else
        worklog = Worklog._make(description, time, issue, day) 

@main.comman()
@click.argument('month')
def send_month(month):
    if 0 < month <= 12:
        pass
    else:
        print('Invalid month (1 to 12)')
        

if __name__ == '__main__':
    main()
