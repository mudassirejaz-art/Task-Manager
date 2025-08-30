import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_list_tasks():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/tasks", json={"title":"test1","description":"x"})
        assert r.status_code == 201
        data = r.json()
        assert data["title"] == "test1"

        r2 = await ac.get("/tasks")
        assert r2.status_code == 200
        tasks = r2.json()
        assert any(t["title"] == "test1" for t in tasks)
