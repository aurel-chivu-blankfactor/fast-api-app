import pytest
from unittest.mock import MagicMock
from app.services.group import (
    create_group,
    get_group,
    get_groups,
    update_group,
    delete_group,
)
from app.schemas.group import GroupCreate, GroupUpdate, Group
from app.models.group import Group as GroupModel
from app.models.user import User
from uuid import uuid4


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_group():
    group = GroupModel(uuid=str(uuid4()), name="Test Group")
    group.users = []
    return group


@pytest.fixture
def mock_user():
    return User(uuid=str(uuid4()), name="Test User", urls={})


@pytest.mark.asyncio
async def test_create_group(mocker, mock_db, mock_group, mock_user):
    mock_group.users = [mock_user]

    mocker.patch("app.services.group.create_group_repo", return_value=mock_group)

    group_data = GroupCreate(name="Test Group")
    result = create_group(mock_db, group_data)

    assert result.name == "Test Group"
    assert result.users == [mock_user.name]
    assert str(result.uuid) == str(mock_group.uuid)


def test_get_group(mocker, mock_db, mock_group, mock_user):
    mock_group.users = [mock_user]

    mocker.patch("app.services.group.get_group_repo", return_value=mock_group)

    result = get_group(mock_db, mock_group.uuid)

    assert result.name == mock_group.name
    assert result.users == [mock_user.name]
    assert str(result.uuid) == str(mock_group.uuid)


def test_get_groups(mocker, mock_db, mock_group, mock_user):
    mock_group.users = [mock_user]

    mocker.patch("app.services.group.get_groups_repo", return_value=[mock_group])

    result = get_groups(mock_db)

    assert len(result) == 1
    assert result[0].name == mock_group.name
    assert result[0].users == [mock_user.name]
    assert isinstance(result[0], Group)


def test_update_group(mocker, mock_db, mock_group):
    mock_group.name = "Updated Group"

    mocker.patch("app.services.group.update_group_repo", return_value=mock_group)

    updated_data = GroupUpdate(name="Updated Group")
    result = update_group(mock_db, mock_group.uuid, updated_data)

    assert result.name == "Updated Group"
    assert str(result.uuid) == str(mock_group.uuid)


def test_delete_group(mocker, mock_db, mock_group):
    mocker.patch("app.services.group.delete_group_repo", return_value=mock_group)

    result = delete_group(mock_db, mock_group.uuid)

    assert result.name == mock_group.name
    assert str(result.uuid) == str(mock_group.uuid)
    assert isinstance(result, Group)
