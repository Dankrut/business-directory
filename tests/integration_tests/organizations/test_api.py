from httpx import AsyncClient


async def test_get_organization_by_id(ac: AsyncClient):
    """Тест получения организации по ID"""
    response = await ac.get("/organizations/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "building" in data
    assert "phones" in data
    assert "activities" in data


async def test_get_organization_not_found(ac: AsyncClient):
    """Тест получения несуществующей организации"""
    response = await ac.get("/organizations/99999")
    assert response.status_code == 404


async def test_get_organizations_by_building(ac: AsyncClient):
    """Тест получения организаций в здании"""
    response = await ac.get("/organizations/building/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # Если есть организации
        assert data[0]["building"]["id"] == 1


async def test_get_organizations_by_building_not_found(ac: AsyncClient):
    """Тест получения организаций в несуществующем здании"""
    response = await ac.get("/organizations/building/99999")
    assert response.status_code == 404


async def test_get_organizations_by_activity(ac: AsyncClient):
    """Тест получения организаций по виду деятельности"""
    response = await ac.get("/organizations/activity/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_organizations_by_activity_not_found(ac: AsyncClient):
    """Тест получения организаций по несуществующей деятельности"""
    response = await ac.get("/organizations/activity/99999")
    assert response.status_code == 404


async def test_get_organizations_nearby(ac: AsyncClient):
    """Тест поиска организаций рядом"""
    response = await ac.get("/organizations/nearby?lat=55.7558&lng=37.6176&radius=1000")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_organizations_nearby_no_results(ac: AsyncClient):
    """Тест поиска организаций рядом (нет результатов)"""
    response = await ac.get("/organizations/nearby?lat=0&lng=0&radius=1")
    assert response.status_code == 404


async def test_search_organizations_by_name(ac: AsyncClient):
    """Тест поиска организаций по названию"""
    response = await ac.get("/organizations/search/name?name=Мясной")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "Мясной" in data[0]["name"]


async def test_search_by_activity_tree(ac: AsyncClient):
    """Тест поиска по дереву деятельности"""
    response = await ac.get("/organizations/search/activity-tree/Еда")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
