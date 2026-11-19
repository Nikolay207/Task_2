import requests
import urls
from helpers import generate_user_data
import allure

@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self):
        user_data = generate_user_data()
        response = requests.post(urls.REGISTER, json=user_data)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == user_data["email"]
        token = response.json()["accessToken"]
        requests.delete(urls.USER, headers={"Authorization": token})

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, registered_user):
        response = requests.post(urls.REGISTER, json={
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        })
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без пароля")
    def test_create_user_without_required_field(self):
        data = {
            "email": "test_without_password@yandex.ru",
            "name": "TestName"}
        response = requests.post(urls.REGISTER, json=data)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "Email, password and name are required fields"