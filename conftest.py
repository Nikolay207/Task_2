import pytest
import requests
import urls
from helpers import generate_user_data

@pytest.fixture()
def registered_user():
    user_data = generate_user_data()
    response = requests.post(urls.REGISTER, json=user_data)
    token = response.json()["accessToken"]
    user_data["accessToken"] = token
    yield user_data
    requests.delete(urls.USER, headers={"Authorization": token})

@pytest.fixture()
def auth_headers(registered_user):
    return {"Authorization": registered_user["accessToken"]}

@pytest.fixture()
def ingredients():
    response = requests.get(urls.INGREDIENTS)
    return [item["_id"] for item in response.json()["data"]]