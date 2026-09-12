import allure
import requests

from config import BASE_URL


@allure.step("POST /orders — создание заказа")
def create_order(payload: dict, headers: dict | None = None) -> requests.Response:
    return requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)


@allure.step("GET /ingredients — получение списка ингредиентов")
def get_ingredients() -> requests.Response:
    return requests.get(f"{BASE_URL}/ingredients")