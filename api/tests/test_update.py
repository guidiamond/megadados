from fastapi.testclient import TestClient
from ..main import app

client: TestClient = TestClient(app)


def test_change_decripton():
    response = client.post("/task?description=test change description original")
    assert response.status_code == 201
    task_id = response.json()["task_id"]

    response = client.get("/task")
    assert response.status_code == 200
    assert task_id in response.json()["tasks"]
    assert response.json()["tasks"][task_id]["description"] == "test change description original"

    response = client.patch(
        "/task/description",
        json={"task_id": task_id, "description": "test change description changed"},
    )
    assert response.status_code == 200
    assert response.json() == {"updated": True}

    response = client.get("/task")
    assert response.status_code == 200
    assert task_id in response.json()["tasks"]
    assert response.json()["tasks"][task_id]["description"] == "test change description changed"

    # Clean up
    response = client.delete(f"/task?task_id={task_id}")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}


def test_change_status():
    response = client.post("/task?description=test change status")
    assert response.status_code == 201
    task_id = response.json()["task_id"]

    response = client.get("/task")
    assert response.status_code == 200
    assert task_id in response.json()["tasks"]
    assert not response.json()["tasks"][task_id]["status"]

    response = client.patch(
        "/task/status",
        json={"task_id": task_id, "status": True},
    )
    assert response.status_code == 200
    assert response.json() == {"updated": True}

    response = client.get("/task")
    assert response.status_code == 200
    assert task_id in response.json()["tasks"]
    assert response.json()["tasks"][task_id]["status"]

    # Clean up
    response = client.delete(f"/task?task_id={task_id}")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}
