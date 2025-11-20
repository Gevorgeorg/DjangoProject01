import pytest
import json
from ads.models import Selection, Ad, Category
from tests.fixtures import auth_data
from tests.factories import AdFactory, CategoryFactory
from django.test import Client


@pytest.mark.django_db
def test_create_ad_simple(client, auth_data: dict) -> None:
    """Тест создания объявления"""

    token: str = auth_data.get('token')
    user_id: int = auth_data.get('user_id')

    category: Category = CategoryFactory()

    ad_data: dict = {
        "name": "Shrecks swamp",
        "price": 100.500,
        "description": "Test",
        "category": category.id,
    }

    response = client.post(
        '/ads/create/',
        data=json.dumps(ad_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    assert response.status_code == 201
    assert Ad.objects.count() == 1

    ad: Ad = Ad.objects.first()
    assert ad.name == "Shrecks swamp"
    assert ad.author.id == user_id
    assert ad.price == 100.500
    assert ad.category == category


@pytest.mark.django_db
def test_create_selection_with_ads(client, auth_data: dict) -> None:
    """Тест создания подборки с объявлениями"""

    token: str = auth_data.get('token')
    user_id: int = auth_data.get('user_id')

    ads: list = AdFactory.create_batch(3)

    selection_data: dict = {
        "name": "Test Selection",
        "items_input": [ad.id for ad in ads]
    }

    response = client.post(
        '/selections/create/',
        data=json.dumps(selection_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    assert response.status_code == 201
    assert Selection.objects.count() == 1

    selection = Selection.objects.first()
    assert selection.name == "Test Selection"
    assert selection.author.id == user_id
    assert selection.items.count() == 3


@pytest.mark.django_db
def test_ads_list() -> None:
    """Тест получения списка объявлений"""

    client = Client()

    AdFactory.create_batch(3)

    response = client.get('/ads/')

    assert response.status_code == 200
    data: dict = response.json()

    assert 'results' in data
    assert len(data['results']) == 3
    assert data['count'] == 3



@pytest.mark.django_db
def test_ad_detail() -> None:
    """Тест получения одного объявления"""

    client = Client()

    ad: Ad = AdFactory()

    response = client.get(f'/ads/{ad.id}/')

    assert response.status_code == 200
    data: dict = response.json()
    assert data.get('name') == ad.name

