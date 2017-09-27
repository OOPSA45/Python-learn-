# coding : utf-8
# Программа клиента, запрашивающего текущее время
from socket import *
import json
import sys


class ClientChat:
    def __init__(self):
        SERVER_HOST = '127.0.0.1'
        SERVER_PORT = 7777
        self.sock = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        self.sock.connect((SERVER_HOST, SERVER_PORT))  # Соединиться с сервером
        self.login = input('Введите логин')
        self.client_presence()
        self.client_auth()

    def client_presence(self):
        json_client_presence_data = {
                    'action': 'presence',
                    'time': '<unix timestamp>',
                    'type': 'status',
                    'user': {
                            'account_name': self.login,
                            'status': 'Yep, I am here!'
                                }
            }
        json_client_presence_data = json.dumps(json_client_presence_data)
        presence_msg = bytes(json_client_presence_data, encoding='utf-8')
        self.sock.send(presence_msg)

    def client_auth(self):
        while True:
            password = input('Введите пароль')
            json_client_auth_data = {
                        'action': 'authenticate',
                        'time': '< unix timestamp >',
                        'user': {
                            'account_name': self.login,
                            'password': password
                                }
            }
            json_client_auth_data = json.dumps(json_client_auth_data)
            auth_msg = bytes(json_client_auth_data, encoding='utf-8')
            self.sock.send(auth_msg)
            answer_from_server = json.loads((str(self.sock.recv(1024), encoding='utf-8')))
            if answer_from_server["response"] == '200':
                print('Go Chat')
            else:
                print(answer_from_server["error"])
                self.__init__()

if __name__ == '__main__':
    ClientChat()
