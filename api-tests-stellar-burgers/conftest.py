import pytest
import requests
import uuid
import time

BASE_URL = "https://stellarburgers.education-services.ru/api"


def generate_unique_user():
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test_{unique_id}_{int(time.time())}@example.com",
        "password": "TestPassword123",
        "name": f"User_{unique_id}"
    }


@pytest.fixture
def new_user_data():
    return generate_unique_user()


@pytest.fixture
def registered_user(new_user_data):
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user_data)
    assert response.status_code == 200, "Не удалось зарегистрировать пользователя"
    data = response.json()
    user = {
        **new_user_data,
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"],
        "user": data["user"]
    }
    yield user
    headers = {"Authorization": user["accessToken"]}
    requests.delete(f"{BASE_URL}/auth/user", headers=headers)


@pytest.fixture
def auth_headers(registered_user):
    return {"Authorization": registered_user["accessToken"]}


@pytest.fixture(scope="session")
def ingredient_ids():
    """Получает актуальные ID ингредиентов с сервера."""
    response = requests.get(f"{BASE_URL}/ingredients")
    assert response.status_code == 200, "Не удалось получить ингредиенты"
    data = response.json()

    ids = [item["_id"] for item in data["data"][:2]]
    assert len(ids) == 2, "Должно быть минимум 2 ингредиента"
    return ids
