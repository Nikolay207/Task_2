import requests
import urls
import allure

@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        response = requests.post(urls.LOGIN, json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_wrong_data(self):
        response = requests.post(urls.LOGIN, json={
            "email": "wrong_email@yandex.ru",
            "password": "wrong_password"
        })
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"