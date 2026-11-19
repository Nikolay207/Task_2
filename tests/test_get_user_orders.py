import requests
import urls
import allure

@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, registered_user, auth_headers):
        ingredients_response = requests.get(urls.INGREDIENTS)
        ingredient_id = ingredients_response.json()["data"][0]["_id"]
        requests.post(urls.ORDERS, json={"ingredients": [ingredient_id]}, headers=auth_headers)
        response = requests.get(urls.ORDERS, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert len(response.json()["orders"]) > 0

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_without_auth(self):
        response = requests.get(urls.ORDERS)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"