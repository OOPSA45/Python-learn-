# coding : utf-8

import sys
from socket import *
import server
import client
import pytest


def test_json_server_response():
    rev = server.json_server_response('200')
    assert rev['alert'] == 'Доступ разрешен'
    rev = server.json_server_response('402')
    assert rev['error'] != 'Доступ разрешен'

# class TestServerChat:
#     def setup(self):
#         print('Я запускаюсь перед каждыйм тестом')
#         server.ServerChat()
#         client.ClientChat()
#         client.ClientChat.login = 'kirill'
#         self.s = server.ServerChat.s
#         server.ServerChat.server_stop(self)
#
#
#     def test_server_presence(self):
#         print(self.s)


# TestServerChat()
test_json_server_response()