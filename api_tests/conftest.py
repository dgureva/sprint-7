import pytest
import requests
import random
import string

from helper.helper import Helper


@pytest.fixture
# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    yield login_pass

    payload = {
        "login": login_pass[0],
        "password": login_pass[1]
    }

    #логиним курьера что бы получить id
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
    response_data = response.json()
    courier_id = response_data['id']

    #удаляем курьера
    response = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')



@pytest.fixture
def generate_random_data():
    helper = Helper()
    login = helper.generate_random_string(10)
    password = helper.generate_random_string(10)
    first_name = helper.generate_random_string(10)
    user_data = []
    user_data.append(login)
    user_data.append(password)
    user_data.append(first_name)
    return user_data