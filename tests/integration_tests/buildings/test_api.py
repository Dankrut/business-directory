from httpx import AsyncClient


async def test_get_buildings(ac: AsyncClient):
    """Тест получения всех зданий"""
    response = await ac.get("/buildings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_building_by_id(ac: AsyncClient):
    """Тест получения здания по ID"""
    response = await ac.get("/buildings/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "address" in data
    assert "latitude" in data
    assert "longitude" in data


async def test_get_building_not_found(ac: AsyncClient):
    """Тест получения несуществующего здания"""
    response = await ac.get("/buildings/99999")
    print(f"\nSTATUS CODE: {response.status_code}")
    print(f"RESPONSE BODY: {response.text}")
    print(f"RESPONSE HEADERS: {response.headers}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Здание не найдено"
