# coding : utf-8

from socket import *
import sys
import json


def json_server_response(code_answer):
    if code_answer != '200':
        return {
            "response": "402",
            "error": "Неверный логин или пароль"
        }
    else:
        return {
            "response": "200",
            "alert": "Доступ разрешен"
        }


class ServerChat:
    def __init__(self):
        SERVER_HOST = '127.0.0.1'
        SERVER_PORT = 7777
        MAX_USERS = 5
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((SERVER_HOST, SERVER_PORT))
        self.s.listen(MAX_USERS)
        print('Сервер чата запущен')
        while True:
            self.result = self.s.accept()
            client, addr = self.result
            print(self.server_presence(client, addr))
            self.server_auth(client)
            self.server_stop()

    def server_presence(self, cl, ad):
        json_client_presence_data = json.loads((str(cl.recv(1024), encoding='utf-8')))
        return ("Получен запрос на соединение от", " ".join(map(str, ad)),
              json_client_presence_data['user']['account_name'], json_client_presence_data['user']['status'])

    def server_auth(self, client_acc):
        json_client_auth_data = json.loads((str(client_acc.recv(1024), encoding='utf-8')))
        if 'kirill' == json_client_auth_data['user']["account_name"]\
                and 'komarov' == json_client_auth_data['user']['password']:
                    self.client_auth('200', client_acc)
                    print('Go chat')
        else:
            self.client_auth('402', client_acc)
            client_acc.close()
            print('Соединение отклонено для', self.result[1])

    def client_auth(self, answer, client):
        json_server_to_client_auth_data = json_server_response(answer)
        json_server_to_client_auth_data = json.dumps(json_server_to_client_auth_data)
        auth_msg = bytes(json_server_to_client_auth_data, encoding='utf-8')
        client.send(auth_msg)

    def server_stop(self):
        self.s.close()
        sys.exit()

if __name__ == '__main__':
    ServerChat()
