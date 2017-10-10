import time
import socket
import json
from server import create_response, get_message


def test_create_response():
    # Нету ключа action
    assert create_response({'one': 'two', 'time': time.time()}) == {'response': 400, 'error': 'Не верный запрос'}
    # Нету ключа time
    assert create_response({'action': 'presence'}) == {'response': 400, 'error': 'Не верный запрос'}
    # Ключ не presence
    assert create_response({'action': 'test_action', 'time': 1000.10}) == {'response': 400, 'error': 'Не верный запрос'}
    # Кривое время
    assert create_response({'action': 'presence', 'time': 'test_time'}) == {'response': 400,
                                                                            'error': 'Не верный запрос'}
    # Всё ок
    assert create_response({'action': 'presence', 'time': 1000.10}) == {'response': 200}


# ИНТЕГРАЦИЯ С КЛИЕНТСКИМ СОКЕТОМ
class ClientSocket():
    """Класс-заглушка для операций с сокетом"""
    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        pass

    def recv(self, n):
        message = {'test': 'test_message'}
        jmessage = json.dumps(message)
        bmessage = jmessage.encode()
        return bmessage


# ИНТЕГРАЦИЯ С КЛИЕНТСКИМ СОКЕТОМ
def test_get_message(monkeypatch):
    """
    Тестим получение сообщения от клиента
    :param monkeypatch: Для подмены любых классов своими заглушками
    """
    monkeypatch.setattr("socket.socket", ClientSocket)
    client = socket.socket()
    assert get_message(client) == {'test': 'test_message'}
