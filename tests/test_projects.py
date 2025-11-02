import pytest
from fastapi.testclient import TestClient


def test_create_project(client: TestClient):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "New Project",
            "description": "Project description",
            "status": "active"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Project"
    assert data["status"] == "active"
    assert "id" in data


def test_get_projects(client: TestClient, sample_project):
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_project_by_id(client: TestClient, sample_project):
    response = client.get(f"/api/v1/projects/{sample_project.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_project.id
    assert data["name"] == sample_project.name


def test_get_project_not_found(client: TestClient):
    response = client.get("/api/v1/projects/99999")
    assert response.status_code == 404


def test_update_project(client: TestClient, sample_project):
    response = client.put(
        f"/api/v1/projects/{sample_project.id}",
        json={
            "name": "Updated Project",
            "status": "completed"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Project"
    assert data["status"] == "completed"


def test_delete_project(client: TestClient, sample_project):
    response = client.delete(f"/api/v1/projects/{sample_project.id}")
    assert response.status_code == 204
    
    response = client.get(f"/api/v1/projects/{sample_project.id}")
    assert response.status_code == 404


def test_filter_projects_by_status(client: TestClient, sample_project):
    response = client.get("/api/v1/projects?status=active")
    assert response.status_code == 200
    data = response.json()
    assert all(project["status"] == "active" for project in data)


def test_search_projects(client: TestClient, sample_project):
    response = client.get(f"/api/v1/projects?search={sample_project.name}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

