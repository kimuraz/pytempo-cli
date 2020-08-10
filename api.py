import requests

BASE_URL = 'https://api.tempo.io/core/3/{}'


def send_worklog(worklog, token):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    print('Sending {}'.format(worklog))
    worklog_dict = {
        'description': worklog.description,
        'timeSpentSeconds': worklog.time * 60,
        'issueKey': worklog.issue,
        'startDate': worklog.day,
    }
    res = requests.post(BASE_URL.format('worklogs'),
                        json=worklog_dict, headers=headers)
    if res.status_code == 200:
        print('Sent.')
        return True
    else:
        print('Failed to send. Status: {}'.format(res.status_code))
        print(res.text)
        return False
