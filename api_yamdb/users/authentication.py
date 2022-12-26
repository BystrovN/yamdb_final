from random import randint
from secrets import token_hex


def generate_confirmation_code():
    '''Сгенерировать код подтверждения для отправки пользователю на email.'''
    len_token = randint(10, 20)
    return token_hex(len_token)
