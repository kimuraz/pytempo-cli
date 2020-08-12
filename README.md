# Tempo CLI

This is a cli project to help managing tasks that needs to be logged on Atlassian's tempo.

> :warning: WIP

Still needs:

- [ ] Interactive activity register #1
- [ ] Proper configuration of setup.py
- [ ] CLI configuration command, to setup config.json
- [ ] Docs
- [ ] Project organisation

## Setting up for development

It's strongly recommended to use `virtualenv`.

```
$ pip install -e .[dev]
```

### Formatting the code

```
$ autopep8 -i filename.py
```

### Config file

The JSON config file should hold a token, the user id on atlassian and the full path where you want the database to be saved, the project uses SQLite.

You can run to create the json file:

```
$ tempo configure -i
# or
$ tempo configure -t your_token -a account_id -d /path/to/db.sqlite3
```

It will save the config file to `$HOME/.tempo/config.json`, by default it's the path to the database as well.

```
{
  "token": "myaw3s0m3t0k3n!",
  "account_id": "id_that_i_found_at_profile_url",
  "db_path": "/some/abs/path/db.sqlite3"
}
```

## Using it

Check the code and just `tempo` to see all the available commands.

```
# Add worklogs: description, time spent in hours and issue code
# Optionally -d "yyyy-mm-dd" for a date other than today

$ tempo work "description" 0.5 "ISSUE-1"

# Listing worklogs
# Optionally -t for today or -m N for a specific month (1 < N < 12)

$ tempo ls

```
