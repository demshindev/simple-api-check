import pytest
from fastapi.testclient import TestClient


def test_create_task(client: TestClient, sample_project):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "New Task",
            "description": "Task description",
            "status": "pending",
            "priority": "high",
            "project_id": sample_project.id
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["project_id"] == sample_project.id
    assert "id" in data


def test_create_task_invalid_project(client: TestClient):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "New Task",
            "project_id": 99999
        }
    )
    assert response.status_code == 404


def test_get_tasks(client: TestClient, sample_task):
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_task_by_id(client: TestClient, sample_task):
    response = client.get(f"/api/v1/tasks/{sample_task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_task.id
    assert data["title"] == sample_task.title


def test_update_task(client: TestClient, sample_task):
    response = client.put(
        f"/api/v1/tasks/{sample_task.id}",
        json={
            "title": "Updated Task",
            "status": "in_progress",
            "priority": "high"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"


def test_delete_task(client: TestClient, sample_task):
    response = client.delete(f"/api/v1/tasks/{sample_task.id}")
    assert response.status_code == 204
    
    response = client.get(f"/api/v1/tasks/{sample_task.id}")
    assert response.status_code == 404


def test_filter_tasks_by_project(client: TestClient, sample_project, sample_task):
    response = client.get(f"/api/v1/tasks?project_id={sample_project.id}")
    assert response.status_code == 200
    data = response.json()
    assert all(task["project_id"] == sample_project.id for task in data)


def test_filter_tasks_by_status(client: TestClient, sample_task):
    response = client.get("/api/v1/tasks?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert all(task["status"] == "pending" for task in data)

