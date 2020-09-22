from typing import Optional, Iterable
from fastapi.testclient import TestClient
from ..main import app

client: TestClient = TestClient(app)


def helper_test_endpoint_dne(
    endpoint: str,
    response_code: int = 404,
    existent: Optional[Iterable] = None,
    nonexistent: Optional[Iterable] = None,
):
    http_methods = {"get", "post", "put", "patch", "delete"}
    if existent is not None:
        if nonexistent is not None:
            raise RuntimeError(
                "helper_test_endpoint_dne called with both existent and nonexistent arguments"
            )
        methods = http_methods ^ set(existent)
    elif nonexistent is not None:
        methods = nonexistent
    else:
        raise RuntimeError(
            "helper_test_endpoint_dne called with neither existent or nonexistent arguments"
        )
    json_responses = {404: {"detail": "Not Found"}, 405: {"detail": "Method Not Allowed"}}
    json_response = json_responses.get(response_code)

    for http_method in methods:
        response = getattr(client, http_method)(endpoint)
        assert response.status_code == response_code
        if json_response:
            assert response.json() == json_response


def test_methods_main_not_found():
    helper_test_endpoint_dne("/", existent=set())


def test_methods_task():
    helper_test_endpoint_dne("/task", 405, existent={"post", "delete"})


def test_methods_tasks():
    helper_test_endpoint_dne("/tasks", 405, existent={"get"})
    helper_test_endpoint_dne("/tasks/done", 405, existent={"get"})
    helper_test_endpoint_dne("/tasks/undone", 405, existent={"get"})
