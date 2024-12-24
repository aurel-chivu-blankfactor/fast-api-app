import pytest
from fastapi.testclient import TestClient


from sqlalchemy.orm import Session

from app.api.user import router as user_router
from app.exceptions.exceptions import UserNotFoundException
from app.schemas.user import User
from app.models.user import User as UserModel
from app.models.group import Group
from uuid import uuid4
from fastapi import FastAPI


app = FastAPI()
app.include_router(user_router)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_user():
    user = UserModel(uuid=str(uuid4()), name="Test User", urls={})
    user.groups = [Group(uuid=str(uuid4()), name="Test Group")]
    return user


@pytest.fixture
def mock_group():
    return Group(uuid=str(uuid4()), name="Test Group")


@pytest.fixture
def mock_user_response(mock_user):
    return User(
        uuid=mock_user.uuid,
        name=mock_user.name,
        urls=mock_user.urls,
        groups=[group.name for group in mock_user.groups],
    )


@pytest.mark.asyncio
async def test_create_user(mocker, client, mock_user, mock_group, mock_user_response):
    mock_create_user_service = mocker.patch(
        "app.api.user.create_user_service", return_value=mock_user_response
    )
    mock_update_user_urls_task = mocker.patch(
        "app.api.user.update_user_urls_task", return_value=None
    )

    user_data = {
        "name": "Test User",
        "urls": {},
        "group_uuid": str(mock_group.uuid),
    }

    response = client.post("/user/", json=user_data)
    assert response.status_code == 200
    result = response.json()

    assert result["name"] == mock_user.name
    assert result["groups"] == [mock_group.name]
    assert "uuid" in result

    mock_create_user_service.assert_called_once()
    mock_update_user_urls_task.assert_called_once()


def test_read_user(mocker, client, mock_user, mock_user_response):

    mock_get_user_service = mocker.patch(
        "app.api.user.get_user_service", return_value=mock_user_response
    )

    response = client.get(f"/user/{mock_user.uuid}")

    assert response.status_code == 200
    result = response.json()
    assert result["name"] == mock_user.name
    assert result["groups"] == [group.name for group in mock_user.groups]
    assert result["uuid"] == str(mock_user.uuid)

    mock_get_user_service.assert_called_once()
    called_args, _ = mock_get_user_service.call_args
    assert isinstance(called_args[0], Session)
    assert str(called_args[1]) == str(mock_user.uuid)


def test_read_user_not_found(mocker, client):

    non_existent_uuid = str(uuid4())

    mock_get_user_service = mocker.patch(
        "app.api.user.get_user_service",
        side_effect=UserNotFoundException(non_existent_uuid),
    )

    response = client.get(f"/user/{non_existent_uuid}")

    assert response.status_code == 404
    result = response.json()
    assert result["error"] == "User not found"
    assert "message" in result

    mock_get_user_service.assert_called_once()


def test_read_users(mocker, client, mock_user, mock_user_response):
    mock_get_users_service = mocker.patch(
        "app.api.user.get_users_service", return_value=[mock_user_response]
    )

    response = client.get("/user/")
    assert response.status_code == 200
    result = response.json()

    assert len(result) == 1
    assert result[0]["name"] == mock_user.name
    assert result[0]["groups"] == [group.name for group in mock_user.groups]
    assert result[0]["uuid"] == str(mock_user.uuid)

    mock_get_users_service.assert_called_once()


def test_update_user(mocker, client, mock_user, mock_user_response):

    mock_user_response.name = "Updated User"

    mock_update_user_service = mocker.patch(
        "app.api.user.update_user_service", return_value=mock_user_response
    )

    updated_data = {"name": "Updated User"}

    response = client.patch(f"/user/{mock_user.uuid}", json=updated_data)

    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Updated User"
    assert result["uuid"] == str(mock_user.uuid)

    mock_update_user_service.assert_called_once()
    called_args, called_kwargs = mock_update_user_service.call_args

    assert isinstance(called_args[0], Session)
    assert str(called_args[1]) == str(mock_user.uuid)
    assert called_args[2].name == "Updated User"


def test_update_user_not_found(mocker, client):

    non_existent_uuid = str(uuid4())

    mock_update_user_service = mocker.patch(
        "app.api.user.update_user_service",
        side_effect=UserNotFoundException(non_existent_uuid),
    )

    updated_data = {"name": "Updated User"}

    response = client.patch(f"/user/{non_existent_uuid}", json=updated_data)

    assert response.status_code == 404
    result = response.json()
    assert result["error"] == "User not found"
    assert "message" in result

    mock_update_user_service.assert_called_once()


def test_delete_user(mocker, client, mock_user):

    mock_delete_user_service = mocker.patch(
        "app.api.user.delete_user_service", return_value=None
    )

    response = client.delete(f"/user/{mock_user.uuid}")

    assert response.status_code == 200
    result = response.json()
    assert (
        result["status"] == f"User with the {mock_user.uuid} was deleted successfully"
    )

    mock_delete_user_service.assert_called_once()
    called_args, _ = mock_delete_user_service.call_args

    assert isinstance(called_args[0], Session)
    assert str(called_args[1]) == str(mock_user.uuid)


def test_delete_user_not_found(mocker, client):

    non_existent_uuid = str(uuid4())

    mock_delete_user_service = mocker.patch(
        "app.api.user.delete_user_service",
        side_effect=UserNotFoundException(non_existent_uuid),
    )

    response = client.delete(f"/user/{non_existent_uuid}")

    assert response.status_code == 404
    result = response.json()
    assert result["error"] == "User not found"
    assert "message" in result

    mock_delete_user_service.assert_called_once()
