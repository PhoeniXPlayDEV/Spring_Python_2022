import time

import flask
from flask import Flask, abort

app = Flask(__name__)
db = []
for i in range(3):
    db.append({
        'name': 'Anton',
        'time': time.time(),
        'text': 'Hi!',
        'flag': 0
    })

def bot(cmd):
    response = {'name': '@Bot', 'text': None, 'time': time.time(), 'flag': 2}
    if cmd == '/help':
        response['text'] = 'Список команд:\n' \
                           '/help - вызывает это сообщение\n' \
                           '/users - выводит список пользователей\n' \
                           '/ping - отвечает сообщением pong\n' \
                           '/messages - выводит количество сообщений\n' \
                           '/messages <дата> - выводит количество сообщений, начиная с указанной даты\n' \
                           '/anonymous - следующее сообщение будет выведено, как анонимное'
    elif cmd == '/users':
        response['text'] = 'Список пользователей: ' + ', '.join(set(m['name'] for m in db if m['flag'] != 2))
    elif cmd == '/ping':
        response['text'] = 'pong'
    elif cmd.startswith('/messages'):
        s = cmd.split(' ')
        amount = 0
        if len(s) == 1:
            for message in db:
                if message['flag'] != 2:
                    amount += 1
            response['text'] = len(db)
        elif len(s) == 2:
            after = float(s[1])
            for message in db:
                if message['time'] > after and message['flag'] != 2:
                    amount += 1
            response['text'] = str(amount)

    if response['text']:
        db.append(response)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/send", methods= ['POST'])
def send_message():
    """
    функция для отправки нового сообщения пользователем
    :return:
    """
    data = flask.request.json
    if not isinstance(data, dict):
        return abort(400)

    if 'name' not in data or \
        'text' not in data:
        return abort(400)

    if not isinstance(data['name'], str) or \
        not isinstance(data['text'], str) or \
        len(data['name']) == 0 or \
        len(data['text']) == 0:
        return abort(400)

    text = data['text']
    name = data['name']
    flag = data['flag']
    message = {
        'text': text,
        'name': name,
        'time': time.time(),
        'flag': flag
    }
    db.append(message)
    if flag != 2:
        bot(text)
    return {'ok': True}

@app.route("/messages")
def get_messages():
    try:
        after = float(flask.request.args['after'])
    except:
        abort(400)
    db_after = []
    for message in db:
        if message['time'] > after:
            db_after.append(message)
    return {'messages': db_after}

@app.route("/status")
def print_status():
    users = set()
    messages_amount = 0
    for m in db:
        if m['flag'] != 2:
            messages_amount += 1
            users.add('<li>' + m['name'] + '</li>')

    return "<p><strong>STATUS WINDOW:</strong></p>" \
           "<p>Amount of users: {users_amount}</p>" \
           "<p>List of users: <ul>{users}</ul></p>" \
           "<p>Amount of messages: {messages_amount}</p>".format(
        users_amount = len(users),
        users = ''.join(users),
        messages_amount = messages_amount
    )

app.run()