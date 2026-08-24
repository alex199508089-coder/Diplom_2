import allure
import requests
from conftest import BASE_URL


@allure.epic("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_authorized_with_ingredients(self, auth_headers, ingredient_ids):
        payload = {"ingredients": ingredient_ids}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "order" in data
        assert "number" in data["order"]

    @allure.title("Создание заказа без авторизации (с валидными ингредиентами)")
    def test_create_order_unauthorized(self, ingredient_ids):
        payload = {"ingredients": ingredient_ids}
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "order" in data
        assert "number" in data["order"]

    @allure.title("Создание заказа с авторизацией, но без ингредиентов")
    def test_create_order_authorized_no_ingredients(self, auth_headers):
        payload = {"ingredients": []}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с авторизацией и невалидным хешем ингредиента")
    def test_create_order_authorized_invalid_hash(self, auth_headers):
        payload = {"ingredients": ["invalid_hash", "another_wrong"]}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)
        assert response.status_code == 500


    @allure.title("Создание заказа с авторизацией и только одним ингредиентом")
    def test_create_order_authorized_one_ingredient(self, auth_headers, ingredient_ids):
        payload = {"ingredients": [ingredient_ids[0]]}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=auth_headers)
        assert response.status_code != 500