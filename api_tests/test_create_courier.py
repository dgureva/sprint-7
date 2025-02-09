import allure
import requests

from helper.helper import Helper

class TestCreateCourier:
    @allure.title("Создание нового курьера")
    def test_create_courier(self, generate_random_data):
        payload = {
            "login": generate_random_data[0],
            "password": generate_random_data[1],
            "firstName": generate_random_data[2]
        }
        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 201

        with allure.step("Проверяем текст ответа"):
            response_text = '{"ok":true}'
            assert response.text == response_text

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cant_create_two_same_couriers(self, generate_random_data):
        payload = {
            "login": generate_random_data[0],
            "password": generate_random_data[1],
            "firstName": generate_random_data[2]
        }
        with allure.step("Отправляем запрос на создание курьера"):
            requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

        with allure.step("Отправляем запрос на создание курьера с теми же данными"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response_data['code'] == 409

        with allure.step("Проверяем текст ответа"):
            expected_message = 'Этот логин уже используется. Попробуйте другой.'
            assert response_data['message'] == expected_message

    @allure.title("Ошибка при создании без логина")
    def test_cant_create_without_login(self, generate_random_data):
        payload = {
            "login": '',
            "password": generate_random_data[1],
            "firstName": generate_random_data[2]
        }
        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 400

        with allure.step("Проверяем текст ответа"):
            response_text = 'Недостаточно данных для создания учетной записи'
            assert response_data['message'] == response_text

    @allure.title("Ошибка при создании без пароля")
    def test_cant_create_without_password(self, generate_random_data):
        payload = {
            "login": generate_random_data[0],
            "password": '',
            "firstName": generate_random_data[2]
        }
        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 400

        with allure.step("Проверяем текст ответа"):
            response_text = 'Недостаточно данных для создания учетной записи'
            assert response_data['message'] == response_text

    @allure.title("Ошибка при создании с существующим логином")
    def test_cant_create_with_already_exist_login(self, register_new_courier_and_return_login_password):
        login, password, first_name = register_new_courier_and_return_login_password
        with allure.step("Подготовка данных"):
            helper = Helper()
            password_2 = helper.generate_random_string(10)
            firstName_2 = helper.generate_random_string(10)
        payload_for_err = {
            "login": login,
            "password": password_2,
            "firstName": firstName_2
        }
        with allure.step("Отправляем запрос на создание курьера c тем же логином"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload_for_err)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 409

        with allure.step("Проверяем текст ответа"):
            response_text = 'Этот логин уже используется. Попробуйте другой.'
            assert response_data['message'] == response_text