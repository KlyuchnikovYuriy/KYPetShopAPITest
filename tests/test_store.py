import allure
import jsonschema
import requests
from .schemas.store_schema import STORE_SCHEMA
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:

    @allure.title("Размещение заказа")
    def test_placing_an_order(self):
        with allure.step("Подготовка данных для создания заказа в магазине"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на создание заказа в магазине"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа: 200"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка содержимого ответа"):
            assert response_json ["id"] == payload['id'], "id не совпадает с ожидаемым"
            assert response_json ["petId"] == payload['petId'], "petId не совпадает с ожидаемым"
            assert response_json ["quantity"] == payload['quantity'], "quantity не совпадает с ожидаемым"
            assert response_json ["status"] == payload['status'], "status не совпадает с ожидаемым"
            assert response_json ["complete"] == payload['complete'], "complete не совпадает с ожидаемым"


    @allure.title("Получение информации о заказе по ID")
    def test_get_order_information_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа: 200"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка что ответ содержит данные заказа с id = 1"):
            assert response.json()["id"] == 1, "ID созданного заказа не совпал с ожидаемым"


    @allure.title("Удаление заказа по ID")
    def test_delete_an_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление питомца по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа: 200"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа: 404"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа: 404"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"


    @allure.title("Получение инвентаря магазина")
    def test_get_receiving_store_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа: 200"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            response_json = response.json()
            jsonschema.validate(response_json, STORE_SCHEMA)

        with allure.step("Проверка содержимого ответа"):
            assert response_json ["approved"] == 57, "approved не совпадает с ожидаемым"
            assert response_json ["delivered"] == 50, "delivered не совпадает с ожидаемым"



