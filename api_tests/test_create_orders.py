import requests
import allure
import pytest

class TestCreateOrder:

    @pytest.mark.parametrize("color", [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([]),
    ],
         ids=(
             "BLACK",
             "GREY",
             "BLACKANDGREY",
             "WITHOUTCOLOR",
         ),
    )
    @allure.title("Содзание заказа")
    def test_create_order(self, color):
        with allure.step("Подготовка данных"):
            payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "Saske, come back to Konoha",
                "color": color
            }

        with allure.step("Отправляем запрос на содзание заказа"):
            response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', json=payload)
            response_data = response.json()

        with allure.step("Проверяем ответ ручки"):
            assert response.status_code == 201

        with allure.step("Проверяем что тело ответа содержит track"):
            assert 'track' in response_data