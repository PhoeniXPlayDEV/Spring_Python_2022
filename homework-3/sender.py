import requests

name = input('Введите имя: ')
while len(name) == 0 or (len(name) >= 1 and name[0] == '@'):
    name = input('Имя не может быть пустым или начинаться с символа @! Введите другое имя: ')
while True:
    flag = 0
    text = input('Введите сообщение: ')
    if text == '/anonymous':
        text = input('Введите анонимное сообщение: ')
        flag = 1

    response = requests.post('http://127.0.0.1:5000/send',
                             json={
                                 'name': name,
                                 'text': text,
                                 'flag': flag
                             }
                            )
