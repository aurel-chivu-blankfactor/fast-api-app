import pytest
from sqlalchemy.orm import Session
from uuid import uuid4
from app.schemas.group import Group, GroupCreate, GroupUpdate


@pytest.fixture
def mock_group():
    return Group(uuid=str(uuid4()), name="Test Group", users=[])


@pytest.fixture
def mock_group_response():
    return {
        "uuid": str(uuid4()),
        "name": "Test Group",
        "users": ["Test User"],
    }


@pytest.fixture
def client():
    from app.main import app
    from fastapi.testclient import TestClient

    return TestClient(app)


def test_create_group(mocker, client, mock_group_response):

    mock_create_group_service = mocker.patch(
        "app.api.group.create_group_service", return_value=mock_group_response
    )

    group_data = {"name": "Test Group"}

    response = client.post("/group/", json=group_data)

    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Test Group"
    assert result["users"] == ["Test User"]

    mock_create_group_service.assert_called_once()
    called_args, _ = mock_create_group_service.call_args
    assert isinstance(called_args[0], Session)
    assert called_args[1].name == "Test Group"


def test_read_group(mocker, client, mock_group, mock_group_response):

    mock_get_group_service = mocker.patch(
        "app.api.group.get_group_service", return_value=mock_group_response
    )

    response = client.get(f"/group/{mock_group.uuid}")

    assert response.status_code == 200
    result = response.json()
    assert result["name"] == mock_group.name
    assert result["users"] == ["Test User"]

    mock_get_group_service.assert_called_once()
    called_args, _ = mock_get_group_service.call_args
    assert isinstance(called_args[0], Session)
    assert str(called_args[1]) == str(mock_group.uuid)


def test_read_groups(mocker, client, mock_group_response):

    mock_get_groups_service = mocker.patch(
        "app.api.group.get_groups_service", return_value=[mock_group_response]
    )

    response = client.get("/group/")

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]["name"] == "Test Group"

    mock_get_groups_service.assert_called_once()
    called_args, _ = mock_get_groups_service.call_args
    assert isinstance(called_args[0], Session)


def test_update_group(mocker, client, mock_group, mock_group_response):

    mock_group_response["name"] = "Updated Group"

    mock_update_group_service = mocker.patch(
        "app.api.group.update_group_service", return_value=mock_group_response
    )

    updated_data = {"name": "Updated Group"}

    response = client.patch(f"/group/{mock_group.uuid}", json=updated_data)

    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Updated Group"

    mock_update_group_service.assert_called_once()
    called_args, _ = mock_update_group_service.call_args
    assert isinstance(called_args[0], Session)
    assert str(called_args[1]) == str(mock_group.uuid)
    assert called_args[2].name == "Updated Group"


def test_delete_group(mocker, client, mock_group):

    mock_delete_group_service = mocker.patch(
        "app.api.group.delete_group_service", return_value=None
    )

    response = client.delete(f"/group/{mock_group.uuid}")

    assert response.status_code == 200
    result = response.json()
    assert (
        result["status"]
        == f"Group with the id {mock_group.uuid} was deleted successfully"
    )

    mock_delete_group_service.assert_called_once()
    called_args, _ = mock_delete_group_service.call_args
    assert isinstance(called_args[0], Session)
    assert str(called_args[1]) == str(mock_group.uuid)
