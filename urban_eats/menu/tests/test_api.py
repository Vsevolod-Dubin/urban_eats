# menu/tests/test_api.py

import pytest

from menu.models import Category, Dish


@pytest.mark.django_db
def test_get_categories_returns_200_and_data(api_client):
    Category.objects.create(name="Soups")
    response = api_client.get("/api/categories/")
    assert response.status_code == 200
    assert response.data[0]["name"] == "Soups"


@pytest.mark.django_db
def test_create_order_without_auth_returns_401(api_client):
    response = api_client.post(
        "/api/orders/", data={"dishes": [1]}, format="json"
    )
    assert response.status_code == 401
    assert "credentials" in str(response.data).lower()


@pytest.mark.django_db
def test_can_create_order_with_auth_returns_201(test_user):
    client, username = test_user
    category = Category.objects.create(name="Drinks")
    dish = Dish.objects.create(name="Coffee", price=2.5, category=category)

    response = client.post(
        "/api/orders/", data={"dishes": [dish.id]}, format="json"
    )
    assert response.status_code == 201
    assert response.data["user"] == username
    assert response.data["dishes"] == [dish.id]


@pytest.mark.django_db
def test_order_with_invalid_dish_id_returns_400(test_user):
    client, _ = test_user
    response = client.post(
        "/api/orders/", data={"dishes": [9999]}, format="json"
    )
    assert response.status_code == 400
    assert "dishes" in response.data
