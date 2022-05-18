from datetime import datetime
from time import sleep

import requests

def print_message(message):
    t = float(message['time'])
    dt = datetime.fromtimestamp(t)
    name = message['name']
    if message['flag'] == 1:
        name = '@Anonymous'
    print('===============================================')
    print(dt.strftime('%Y-%m-%d %H:%M:%S'), name)
    print(message['text'])
    print('===============================================')
    print()

after = 0
while True:
    response = requests.get(
        'http://127.0.0.1:5000/messages',
                            params={'after': after})
    messages = response.json()['messages']
    for message in messages:
        print_message(message)
    after = message['time']
    sleep(1)