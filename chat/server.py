# coding : utf-8
# Программа сервера времени
from socket import *
import time


class ServerChat:
    def __init__(self):
        SERVER_HOST = '127.0.0.1'
        SERVER_PORT = 7777
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((SERVER_HOST, SERVER_PORT))
        self.s.listen(5)
        print(self.s.listen())
        result = self.s.accept()
        client, addr = result
        print("Получен запрос на соединение от", " ".join(map(str, addr)))
        try:
            self.echo_to_client = f'{"Подключение успешно к:"} \n ' \
                                  f'{SERVER_HOST} {SERVER_PORT} \n {time.ctime(time.time())}'
        except:
            print('Подключение не удалось')
        while True:
            self.echo_to_client = bytes(str(self.echo_to_client), encoding='utf-8')
            client.send(self.echo_to_client)
            data = client.recv(1024)
            print(str(data, encoding='utf-8'))


ServerChat()
