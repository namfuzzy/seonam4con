import pytest


async def login(client):
    response = await client.post(
        "/api/v1/auth/login", json={"email": "admin@example.com", "password": "Admin123!"}
    )
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


@pytest.mark.asyncio
async def test_create_project_flow(client):
    token = await login(client)

    response = await client.post(
        "/api/v1/projects/",
        json={"name": "Dự án mới", "goals": "Kiểm thử", "owner_id": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201, response.text
    project = response.json()
    assert project["name"] == "Dự án mới"

    response = await client.get(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    items = response.json()
    assert any(item["name"] == "Dự án mới" for item in items)
