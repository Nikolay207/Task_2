from uuid import uuid4

def generate_user_data():
    return {
        "email": f"test_{uuid4()}@yandex.ru",
        "password": "123456",
        "name": "TestUser",
    }
