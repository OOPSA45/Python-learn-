"""
Функции ​​сервера:​
- принимает ​с​ообщение ​к​лиента;
- формирует ​​ответ ​к​лиенту;
- отправляет ​​ответ ​к​лиенту;
- имеет ​​параметры ​к​омандной ​с​троки:
- -p ​​<port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт ​​7777);
- -a ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса).
"""
import sys
import select
import time
import json
from socket import socket, AF_INET, SOCK_STREAM
from functools import wraps
from log_config import logger


class Log:

    def __call__(self, func):
        ''' Декоратор-замедлитель
        '''
        @wraps(func)
        def decorated(*args, **kwargs):
            ''' Декорированная функция
            '''
            res = func(*args, **kwargs)
            print(func.__name__)
            logger.info('Тест сервера')
            return res
        return decorated

@Log()
def get_message(client):
    """
    Получение ответа от клиента
    :param client: Клиентский сокет
    :return: Словарь ответа
    """
    # Получаем ответ в байтах
    bresponse = client.recv(1024)
    # декодируем получаем json
    jresponse = bresponse.decode('utf-8')
    # преобразуем json в словарь
    response = json.loads(jresponse)
    return response

@Log()
def send_response(message, client):
    """
    Отправка ответа клиенту
    :param message: словарь сообщения
    :param client: Клиентский сокет
    :return: None
    """
    # Словарь переводим в json
    jmessage = json.dumps(message)
    # Строку в байты
    bmessage = jmessage.encode('utf-8')
    # Отправляем
    client.send(bmessage)

@Log()
def create_response(presence_message):
    """
    Формирование ответа клиенту
    :param presence_message: Словарь presence запроса
    :return:
    """
    # Делаем проверки
    if 'action' in presence_message and \
                    presence_message['action'] == 'presence' and \
                    'time' in presence_message and \
                    isinstance(presence_message['time'], float):
        # Если всё хорошо шлем ОК
        return {'response': 200}
    else:
        # Шлем код ошибки
        return {'response': 400, 'error': 'Не верный запрос'}


if __name__ == '__main__':
    print('Запуск сервера')
    address = ('', 7777)
    clients = []
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    sock.settimeout(0.2)   # Таймаут для операций с сокетом
        # Таймаут необходим, чтобы выполнять разные действия с сокетом:
        #  - проверить сокет на наличие подключений новых клиентов
        #  - проверить сокет на наличие данных
    while True:
        try:
            conn, addr = sock.accept()  # Проверка подключений
        except OSError as e:
            pass
        else:
            if clients.count(conn) == 0:
                print("Получен запрос на соединение с %s" % str(addr))
                presence_message = get_message(conn)
                print('Клиент отправил {}'.format(presence_message))
                # формируем ответ
                response = create_response(presence_message)
                # отправляем ответ клиенту
                send_response(response, conn)
                clients.append(conn)
                print(clients)
        finally:
                # Проверить наличие событий ввода-вывода без таймаута
            w = []
            try:
                r, w, e = select.select([], clients, [], 0)
            except Exception as e:
                    # Исключение произойдёт, если какой-то клиент отключится
                pass  # Ничего не делать, если какой-то клиент отключился
                # Обойти список клиентов, читающих из сокета
            for s_client in w:
                try:
                    s_client.settimeout(0.2)
                    msg = s_client.recv(1024)
                except:
                    msg = ''
                finally:
                    try:
                        if msg != '':
                            for s_client in w:
                                s_client.settimeout(0.2)
                                s_client.send(msg)
                    except:
                        # Удаляем клиента, который отключился
                        clients.remove(s_client)
                        print('Delete')
                msg = ''
