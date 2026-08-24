import allure
import requests
from conftest import BASE_URL


@allure.epic("Логин пользователя")
class TestLogin:

    @allure.title("Успешный вход существующего пользователя")
    def test_login_existing_user(self, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        assert data["accessToken"].startswith("Bearer ")
        assert "refreshToken" in data
        assert data["user"]["email"] == registered_user["email"]
        assert data["user"]["name"] == registered_user["name"]

    @allure.title("Вход с неверным логином")
    def test_login_wrong_email(self, registered_user):
        login_data = {
            "email": "wrong@example.com",
            "password": registered_user["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "email or password are incorrect"

    @allure.title("Вход с неверным паролем")
    def test_login_wrong_password(self, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": "WrongPassword"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "email or password are incorrect"

    @allure.title("Вход с отсутствующим паролем")
    def test_login_missing_password(self, registered_user):
        login_data = {
            "email": registered_user["email"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "email or password are incorrect"