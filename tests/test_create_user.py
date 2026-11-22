import requests
import urls
import allure


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, auth_headers, ingredients):
        with allure.step("Отправка POST-запроса на создание заказа"):
            response = requests.post(urls.ORDERS, json={
                "ingredients": [ingredients[0], ingredients[1]]
            }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()
        assert "number" in response.json()["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, ingredients):
        with allure.step("Отправка POST-запроса на создание заказа без токена"):
            response = requests.post(urls.ORDERS, json={
                "ingredients": [ingredients[0], ingredients[1]]
            })
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, auth_headers):
        with allure.step("Отправка POST-запроса с пустым списком ингредиентов"):
            response = requests.post(urls.ORDERS, json={
                "ingredients": []
            }, headers=auth_headers)
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным id ингредиентов")
    def test_create_order_with_invalid_hash(self):
        with allure.step("Отправка POST-запроса с несуществующим id ингредиента"):
            response = requests.post(urls.ORDERS, json={
                "ingredients": ["invalid_123"]
            })
        assert response.status_code == 500