import allure
import requests

from config import BASE_URL


@allure.step("POST /auth/register — регистрация пользователя")
def register_user(user_data: dict) -> requests.Response:
    return requests.post(f"{BASE_URL}/auth/register", json=user_data)


@allure.step("POST /auth/login — авторизация пользователя")
def login_user(login_data: dict) -> requests.Response:
    return requests.post(f"{BASE_URL}/auth/login", json=login_data)


@allure.step("DELETE /auth/user — удаление пользователя")
def delete_user(headers: dict) -> requests.Response:
    return requests.delete(f"{BASE_URL}/auth/user", headers=headers)