import time
import uuid

import pytest

from api.auth_api import delete_user, register_user
from api.orders_api import get_ingredients


class SetupFailedError(RuntimeError):
    """Ошибка подготовки тестовых данных (окружение, а не функциональность)."""


def _generate_unique_user() -> dict:
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test_{unique_id}_{int(time.time())}@example.com",
        "password": "TestPassword123",
        "name": f"User_{unique_id}",
    }


@pytest.fixture
def new_user_data() -> dict:
    return _generate_unique_user()


@pytest.fixture
def registered_user(new_user_data):
    response = register_user(new_user_data)
    if response.status_code != 200:
        raise SetupFailedError(
            f"Не удалось зарегистрировать пользователя. "
            f"Код: {response.status_code}, тело: {response.text}"
        )

    data = response.json()
    user = {
        **new_user_data,
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"],
        "user": data["user"],
    }
    yield user

    try:
        delete_user({"Authorization": user["accessToken"]})
    except Exception:
        pass


@pytest.fixture
def auth_headers(registered_user) -> dict:
    return {"Authorization": registered_user["accessToken"]}


@pytest.fixture(scope="session")
def ingredient_ids() -> list[str]:
    response = get_ingredients()
    if response.status_code != 200:
        raise SetupFailedError(
            f"Не удалось получить ингредиенты. Код: {response.status_code}"
        )

    data = response.json()
    ids = [item["_id"] for item in data["data"][:2]]
    if len(ids) < 2:
        raise SetupFailedError(
            f"Ожидалось минимум 2 ингредиента, получено: {len(ids)}"
        )
    return ids
