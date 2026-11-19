import requests
import urls
from helpers import generate_user_data
import allure

@allure.feature("Изменение данных пользователя")
class TestUpdateUser:

    @allure.title("Обновление данных с авторизацией")
    def test_update_user_with_auth(self, registered_user, auth_headers):
        new_data = generate_user_data()
        response = requests.patch(urls.USER, json={
            "email": new_data["email"],
            "name": "NewName"
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["name"] == "NewName"
        assert response.json()["user"]["email"] == new_data["email"]

    @allure.title("Обновление данных без авторизации")
    def test_update_user_without_auth(self):
        response = requests.patch(urls.USER, json={
            "name": "NewName"})
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"