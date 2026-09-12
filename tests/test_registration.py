import allure
from api.auth_api import register_user



@allure.epic("Регистрация пользователя")
class TestRegistration:

    @allure.title("Успешная регистрация нового пользователя")
    def test_register_new_user_success(self, new_user_data):
        response = register_user(new_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        assert data["accessToken"].startswith("Bearer ")
        assert "refreshToken" in data
        assert data["user"]["email"] == new_user_data["email"]
        assert data["user"]["name"] == new_user_data["name"]

    @allure.title("Регистрация уже существующего пользователя")
    def test_register_existing_user(self, registered_user):
        user_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"],
        }
        response = register_user(user_data)
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "User already exists"

    @allure.title("Регистрация без обязательного поля password")
    def test_register_missing_password(self, new_user_data):
        incomplete_data = {
            "email": new_user_data["email"],
            "name": new_user_data["name"],
        }
        response = register_user(incomplete_data)
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"

    @allure.title("Регистрация без обязательного поля email")
    def test_register_missing_email(self, new_user_data):
        incomplete_data = {
            "password": new_user_data["password"],
            "name": new_user_data["name"],
        }
        response = register_user(incomplete_data)
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"
