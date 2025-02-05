import requests
import allure


class TestOrderList():
    @allure.title("В тело ответа возвращается список заказов")
    def test_order_list_return_list(self):
        with allure.step("Отправляем запрос на получения списка заказов"):
            response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders?limit=10&page=0&nearestStation=["110"]')
            response_data = response.json()
        with allure.step("Проверяем, что в тело ответа возвращается список заказов"):
            assert response.status_code == 200
            assert 'orders' in response_data
            assert isinstance(response_data['orders'], list)