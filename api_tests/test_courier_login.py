import requests
import allure


class TestLogIn:
    @allure.title("Логин курьера")
    def test_log_in_courier(self, register_new_courier_and_return_login_password):
        with allure.step("Подготовка данных"):
            courier_data = register_new_courier_and_return_login_password
            payload = {
                "login": courier_data[0],
                "password": courier_data[1]
            }
        with allure.step("Отправляем запрос на логин курьера"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 200

        with allure.step("Проверяем наличие id в ответе"):
            assert 'id' in response_data

    @allure.title("Логин курьера без логина")
    def test_log_in_courier_without_login(self, register_new_courier_and_return_login_password):
        with allure.step("Подготовка данных"):
            courier_data = register_new_courier_and_return_login_password
            payload = {
                "login": '',
                "password": courier_data[1]
            }
        with allure.step("Отправляем запрос на логин курьера"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 400

        with allure.step("Проверяем текст ответа"):
            response_text = 'Недостаточно данных для входа'
            assert response_data['message'] == response_text


    @allure.title("Логин курьера без пароля")
    def test_log_in_courier_without_pwd(self, register_new_courier_and_return_login_password):
        with allure.step("Подготовка данных"):
            courier_data = register_new_courier_and_return_login_password
            payload = {
                "login": courier_data[0],
                "password": ''
            }
        with allure.step("Отправляем запрос на логин курьера"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 400

        with allure.step("Проверяем текст ответа"):
            response_text = 'Недостаточно данных для входа'
            assert response_data['message'] == response_text

    @allure.title("Логин не сушествующего курьера")
    def test_log_in_non_existent_courier(self, generate_random_data):
        payload = {
            "login": generate_random_data[0],
            "password": generate_random_data[1],
            "firstName": generate_random_data[2]
        }

        with allure.step("Отправляем запрос на логин курьера"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 404

        with allure.step("Проверяем текст ответа"):
            response_text = 'Учетная запись не найдена'
            assert response_data['message'] == response_text