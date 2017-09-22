# coding : utf-8
# Программа клиента, запрашивающего текущее время
from socket import *
import json
import sys


class ClientChat:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        self.sock.connect(('localhost', 7777))  # Соединиться с сервером
        tm = self.sock.recv(1024)  # Принять не более 1024 байтов данных
        json_client_data = {
                    'action': 'authenticate',
                    'time': '< unix timestamp >',
                    'user': {
                        'account_name': 'C0deMaver1ck',
                        'password': 'CorrectHorseBatterStaple'
                            }
        }
        print(str(tm, encoding='utf-8'))
        self.json_data = json.dumps(json_client_data)
        while True:
            move = input('Введите сообщение')
            if move == 'q':
                self.client_close
            else:
                self.client_send_msg(move)

    @property
    def client_close(self):
        print('Выход из программы')
        sys.exit()

    def client_send_msg(self, msg):
        msg = '{0} \n {1}'.format(self.json_data, msg)
        msg = bytes(msg, encoding='utf-8')
        self.sock.send(msg)


ClientChat()
