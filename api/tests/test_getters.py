from fastapi.testclient import TestClient
from ..main import app

client: TestClient = TestClient(app)


def test_listall_delete():
    response = client.post("/task?description=test listall delete")
    assert response.status_code == 201
    task_id = response.json()["task_id"]

    response = client.get("/task")
    assert response.status_code == 200
    assert task_id in response.json()["tasks"]
    assert response.json()["tasks"][task_id]["description"] == "test listall delete"

    # Clean up
    response = client.delete(f"/task?task_id={task_id}")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}


def test_listall_delete_many():
    task_ids = []
    for i in range(10):
        response = client.post(f"/task?description=test listall delete many {i}")
        assert response.status_code == 201
        task_ids.append(response.json()["task_id"])

    response = client.get("/task")
    assert response.status_code == 200

    for i, task_id in enumerate(task_ids):
        assert task_id in response.json()["tasks"]
        assert response.json()["tasks"][task_id]["description"] == f"test listall delete many {i}"

    # Clean up
    for task_id in task_ids:
        response = client.delete(f"/task?task_id={task_id}")
        assert response.status_code == 200
        assert response.json() == {"deleted": True}


def test_change_status_list():
    task_ids = []
    for i in range(10):
        response = client.post(f"/task?description=test status list {i}")
        assert response.status_code == 201
        task_ids.append(response.json()["task_id"])

    response = client.get("/task")
    assert response.status_code == 200

    for i in range(7):
        response = client.patch(
            "/task/status",
            json={"task_id": task_ids[i], "status": True},
        )
        assert response.status_code == 200
        assert response.json() == {"updated": True}

    response = client.get("/task/done")
    assert response.status_code == 200
    tasks_done = response.json()["tasks"]

    response = client.get("/task/undone")
    assert response.status_code == 200
    tasks_undone = response.json()["tasks"]

    for i in range(7):
        assert task_ids[i] in tasks_done
        assert task_ids[i] not in tasks_undone
        item = tasks_done[task_ids[i]]
        assert item["status"]
        assert item["description"] == f"test status list {i}"

    for i in range(7, 10):
        assert task_ids[i] not in tasks_done
        assert task_ids[i] in tasks_undone
        item = tasks_undone[task_ids[i]]
        assert not item["status"]
        assert item["description"] == f"test status list {i}"

    # Clean up
    for task_id in task_ids:
        response = client.delete(f"/task?task_id={task_id}")
        assert response.status_code == 200
        assert response.json() == {"deleted": True}
