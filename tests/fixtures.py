import pytest
import json
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def auth_data(client) -> dict:
    """Создает пользователя и возвращает токен"""

    user_data: dict = {
        "username": "testuser",
        "password": "testpass",
        "last_name": "Test",
        "birth_date": "2000-01-01",
        "first_name": "User",
        "role": "member",
        "age": 25,
        "email": "test@test.com"
    }

    user_response = client.post('/users/create/',
                                data=json.dumps(user_data),
                                content_type='application/json')

    user_id: int = user_response.json().get('id')

    token_response = client.post('/token/',
                                 data=json.dumps({"username": user_data.get("username"),
                                                  "password": user_data.get("password")}),
                                 content_type='application/json')

    token: str = token_response.json().get('access')

    return {
        'token': token,
        'user_id': user_id,
        'user_data': user_data
    }
