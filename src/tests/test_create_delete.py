from fastapi.testclient import TestClient
from ..main import app

client: TestClient = TestClient(app)


def test_create_delete():
    response = client.post("/task?description=test create delete")
    assert response.status_code == 201
    task_id = response.json()["task_id"]

    response = client.delete(f"/task?task_id={task_id}")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}


def test_create_delete_listall():
    response = client.post("/task?description=test create delete listall")
    assert response.status_code == 201
    task_id = response.json()["task_id"]

    response = client.delete(f"/task?task_id={task_id}")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}

    response = client.get("/tasks")
    assert response.status_code == 200
    assert task_id not in response.json()["tasks"]
