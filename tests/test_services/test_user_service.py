import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.user import (
    fetch_github_data,
    create_user,
    update_user_urls_task,
    get_user,
    get_users,
    update_user,
    delete_user,
)
from app.schemas.user import UserCreate, UserUpdate, User
from app.models.user import User as UserModel
from app.models.group import Group
from uuid import uuid4


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_user():
    user = UserModel(uuid=str(uuid4()), name="Test User", urls={})
    user.groups = []
    return user


@pytest.fixture
def mock_group():
    return Group(uuid=str(uuid4()), name="Test Group")


@pytest.fixture
def mock_github_response():
    return {
        "current_user_url": "https://api.github.com/{user}",
        "followers_url": "https://api.github.com/{user}/followers",
    }


@pytest.mark.asyncio
async def test_fetch_github_data(mocker, mock_github_response):
    mocker.patch(
        "httpx.AsyncClient.get",
        return_value=AsyncMock(status_code=200, json=lambda: mock_github_response),
    )
    user_uuid = str(uuid4())

    result = await fetch_github_data(user_uuid)

    assert result["current_user_url"] == f"https://api.github.com/{user_uuid}"
    assert result["followers_url"] == f"https://api.github.com/{user_uuid}/followers"


@pytest.mark.asyncio
async def test_create_user(mocker, mock_db, mock_user, mock_group):

    mock_user.groups = [mock_group]

    user_uuid = str(mock_user.uuid)
    mock_github_response = {
        "current_user_url": f"https://api.github.com/{user_uuid}",
        "followers_url": f"https://api.github.com/{user_uuid}/followers",
    }

    mocker.patch("app.services.user.create_user_repo", return_value=mock_user)
    mocker.patch(
        "app.services.user.fetch_github_data", return_value=mock_github_response
    )

    user_data = UserCreate(name="Test User", urls={}, group_uuid=mock_group.uuid)
    result = await create_user(mock_db, user_data)

    assert result.name == "Test User"
    assert result.groups == [mock_group.name]
    assert result.urls["current_user_url"] == f"https://api.github.com/{user_uuid}"
    assert (
        result.urls["followers_url"] == f"https://api.github.com/{user_uuid}/followers"
    )


@pytest.mark.asyncio
async def test_update_user_urls_task(mocker, mock_db, mock_user, mock_github_response):
    """Test updating user URLs asynchronously."""
    mocker.patch(
        "app.services.user.fetch_github_data", return_value=mock_github_response
    )
    mocker.patch("app.repository.user.update_user_urls", return_value=None)

    await update_user_urls_task(mock_db, mock_user.uuid)

    mock_db.query.assert_called_once()
    assert mock_db.commit.called


def test_get_user(mocker, mock_db, mock_user):
    mocker.patch("app.services.user.get_user_repo", return_value=mock_user)

    result = get_user(mock_db, mock_user.uuid)

    assert result.name == mock_user.name
    assert str(result.uuid) == str(mock_user.uuid)
    assert result.urls == mock_user.urls
    assert result.groups == [group.name for group in mock_user.groups]


def test_get_users(mocker, mock_db, mock_user):
    mocker.patch("app.services.user.get_users_repo", return_value=[mock_user])

    result = get_users(mock_db)

    assert len(result) == 1
    assert result[0].name == mock_user.name
    assert isinstance(result[0], User)


def test_update_user(mocker, mock_db, mock_user):
    mock_user.name = "Updated User"

    mocker.patch("app.services.user.update_user_repo", return_value=mock_user)

    updated_data = UserUpdate(name="Updated User")

    result = update_user(mock_db, mock_user.uuid, updated_data)

    assert result.name == "Updated User"
    assert str(result.uuid) == str(mock_user.uuid)


def test_delete_user(mocker, mock_db, mock_user):
    mocker.patch("app.services.user.delete_user_repo", return_value=mock_user)

    result = delete_user(mock_db, mock_user.uuid)

    assert str(result.uuid) == str(mock_user.uuid)
    assert result.name == mock_user.name
    assert isinstance(result, User)
