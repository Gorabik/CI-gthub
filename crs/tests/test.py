import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from routes import app
from fastapi.testclient import TestClient

client = TestClient(app)

import asyncio
from database import engine, Base

def reset_db():
    async def _reset():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(_reset())

def test_get_empty_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []

def test_create_app():
    response = client.post('/recipes', json={'name': 'Борщ',
     'minutes': 10, 'ingredients':'Свекла, Капуста',
     'description': 'some ingredients'})
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['message'] == 'Рецепт успешно создан'

    response2 = client.post(
        '/recipes',
        json={
            'name': 'Куриный суп',
            'minutes': 8,
            'ingredients': 'Курица, Вода',
            'description': 'Chicken for cooking very delicious'
        }
    )
    assert response2.status_code == 200
    assert response2.json() == {'detail': 'Recipe already exists'}


def test_get_recipe():
    response = client.get("/recipes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Борщ"
    assert data["views"] >= 1
    assert "ingredients" in data
    assert "description" in data

def test_get_recipe_detail():
    response = client.get("/recipes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Борщ"
    assert data["views"] >= 1
    assert "ingredients" in data
    assert "description" in data

def test_no_dishes():
    response = client.get("/recipes/987")
    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}

def test_duplicate():
    response = client.post(
     "/recipes",
     json={"name": "Борщ", "minutes": 10, "ingredients": 'Свекла, Капуста',
          "description": 'some ingredients'},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Recipe already exists"

def test_create_existing_item():
    response = client.post(
        "/recipes",
        json={
            "name": "Борщ",
            "minutes": 10,
            "ingredients": "Свекла, Капуста",
            "description": "some ingredients for cooking"
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Recipe already exists"}


if __name__ == "__main__":

    reset_db()
    test_get_empty_recipes()
    print("test_get_empty_recipes passed")


    test_get_recipe()
    print("test_get_recipes_after_create passed")

    test_get_recipe_detail()
    print("test_get_recipe_detail passed")

    test_no_dishes()
    print("test_get_nonexistent_recipe passed")

    test_duplicate()
    print("test_create_duplicate_recipe passed")

    print("\n All tests passed!")
