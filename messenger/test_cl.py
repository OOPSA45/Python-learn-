import time
import json
from pytest import raises
from client import create_presence_message, translate_message
from errors import UsernameToLongError, ResponseCodeLenError, MandatoryKeyError, ResponseCodeError


def test_create_presence_message():
    # без параметров
    message = create_presence_message()
    assert message['action'] == "presence"
    # берем разницу во времени
    assert abs(message['time'] - time.time()) < 0.1
    assert message["user"]["account_name"] == 'Guest'
    # с именем
    message = create_presence_message('test_user_name')
    assert message["user"]["account_name"] == 'test_user_name'
    # неверный тип
    with raises(TypeError):
        create_presence_message(200)
    with raises(TypeError):
        create_presence_message(None)
    # Имя пользователя слишком длинное
    with raises(UsernameToLongError):
        create_presence_message('11111111111111111111111111')


def test_translate_message():
    # неверная длина кода ответа
    with raises(ResponseCodeLenError):
        translate_message({'response': '5'})
    # нету ключа response
    with raises(MandatoryKeyError):
        translate_message({'one': 'two'})
    # неверный код ответа
    with raises(ResponseCodeError):
        translate_message({'response': 700})
    # все правильно
    assert translate_message({'response': 200}) == {'response': 200}


