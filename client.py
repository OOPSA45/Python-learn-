"""
Функции ​к​лиента:​
- сформировать ​​presence-сообщение;
- отправить ​с​ообщение ​с​ерверу;
- получить ​​ответ ​с​ервера;
- разобрать ​с​ообщение ​с​ервера;
- параметры ​к​омандной ​с​троки ​с​крипта ​c​lient.py ​​<addr> ​[​<port>]:
- addr ​-​ ​i​p-адрес ​с​ервера;
- port ​-​ ​t​cp-порт ​​на ​с​ервере, ​​по ​у​молчанию ​​7777.
"""
import sys
import time
import json
from socket import socket, AF_INET, SOCK_STREAM
from errors import UsernameToLongError, ResponseCodeLenError, MandatoryKeyError, ResponseCodeError


def create_presence_message(account_name="Guest"):
    """
    Сформировать ​​presence-сообщение
    :param account_name: Имя пользователя
    :return: Словарь сообщения
    tests:
    ИЗ-ЗА времени нельзя написать doctest
    """
    if not isinstance(account_name, str):
        raise TypeError
    if len(account_name) > 25:
        raise UsernameToLongError(account_name)
    message = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "account_name": account_name
        }
    }
    return message


def send_message(message, sock):
    """
    Отправка сообщения серверу
    :param message: Словарь сообщения
    :param sock: Сокет
    :return: None
    """
    # Преобразуем словарь в json
    jmessage = json.dumps(message)
    # Переводим json в байты
    bmessage = jmessage.encode('utf-8')
    # Отправляем байты
    sock.send(bmessage)


def get_response(sock):
    """
    Получение ответа от сервера
    :param sock: Сокет
    :return: Словарь ответа
    """
    # Получаем ответ
    bresponse = sock.recv(1024)
    # Декодируем байты в json
    jresponse = bresponse.decode('utf-8')
    # Получаем из json словарь
    response = json.loads(jresponse)
    return response


def translate_message(response):
    """
    Разбор сообщения
    :param response: Словарь ответа от сервера
    :return: корректный словарь ответа
    """
    # Нету ключа response
    if 'response' not in response:
        raise MandatoryKeyError('response')
    code = str(response['response'])
    # длина кода не 3 символа
    if len(code) != 3:
        raise ResponseCodeLenError(code)
    # неправильные коды символов
    if code[0] not in '1245':
        raise ResponseCodeError(code)
    return response


if __name__ == '__main__':
    posab = input('Введите функцию клиента(-r/-w) на чтение / на написание сообщений')
    print('Клиент запущен с функцией', posab)
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    # Пытаемся получить параметры скрипта
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = 'localhost'
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)
    # Соединиться с сервером
    s.connect((addr, port))
    # Создаем сообщение
    presence_message = create_presence_message()
    # Отсылаем сообщение
    send_message(presence_message, s)
    # Получаем ответ
    response = get_response(s)
    # Проверяем ответ
    response = translate_message(response)
    print('Сервер ответил')
    print(response)
    if posab == "-r":
        while True:
            tm = s.recv(1024)  # Принять не более 1024 байтов данных
            print(tm.decode('ascii'))
        s.close()
    else:
        while True:
            msg = input('Enter msg')
            msg = msg.encode('utf-8')
            s.send(msg)
    s.close()
