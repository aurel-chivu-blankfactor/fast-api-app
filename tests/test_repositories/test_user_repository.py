import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.repository.user import (
    create_user,
    update_user_urls,
    get_user,
    get_users,
    update_user,
    delete_user,
)
from app.exceptions.group_not_found_exception import GroupNotFoundException
from app.exceptions.user_not_found_exception import UserNotFoundException
from app.models.user import User
from app.models.group import Group
from app.schemas.user import UserCreate


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_group():
    return Group(uuid=str(uuid4()), name="Test Group")


@pytest.fixture
def mock_user(mock_group):
    return User(
        uuid=str(uuid4()),
        name="Test User",
        urls={},
        groups=[mock_group],
    )


def test_create_user_success(mock_session, mock_group):
    mock_session.query.return_value.filter.return_value.first.return_value = mock_group
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()

    user_data = UserCreate(name="New User", urls={}, group_uuid=mock_group.uuid)
    new_user = create_user(mock_session, user_data)

    assert new_user.name == "New User"
    assert new_user.groups[0] == mock_group
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_create_user_group_not_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = None

    user_data = UserCreate(name="New User", urls={}, group_uuid=str(uuid4()))
    with pytest.raises(GroupNotFoundException):
        create_user(mock_session, user_data)


def test_update_user_urls_success(mock_session, mock_user):
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user

    new_urls = {"github": "https://github.com/testuser"}
    updated_user = update_user_urls(mock_session, mock_user.uuid, new_urls)

    assert updated_user.urls == new_urls
    mock_session.commit.assert_called_once()


def test_get_user_success(mock_session, mock_user):
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user

    fetched_user = get_user(mock_session, mock_user.uuid)

    assert fetched_user == mock_user


def test_get_user_not_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(UserNotFoundException):
        get_user(mock_session, str(uuid4()))


def test_get_users(mock_session, mock_user):
    mock_session.query.return_value.all.return_value = [mock_user]

    users = get_users(mock_session)

    assert len(users) == 1
    assert users[0] == mock_user


def test_update_user_success(mock_session, mock_user, mock_group):

    mock_session.query.return_value.filter.return_value.first.side_effect = [mock_user]

    mock_session.query.return_value.filter.return_value.all.return_value = [mock_group]

    new_data = {"name": "Updated User", "groups": [mock_group.name]}

    updated_user = update_user(mock_session, mock_user.uuid, new_data)

    assert updated_user.name == "Updated User"
    assert updated_user.groups == [mock_group]
    mock_session.commit.assert_called_once()


def test_update_user_group_not_found(mock_session, mock_user):
    mock_session.query.return_value.filter.return_value.first.side_effect = [
        mock_user,
        None,
    ]

    new_data = {"groups": ["Nonexistent Group"]}
    with pytest.raises(GroupNotFoundException):
        update_user(mock_session, mock_user.uuid, new_data)


def test_delete_user_success(mock_session, mock_user):
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user

    deleted_user = delete_user(mock_session, mock_user.uuid)

    assert deleted_user == mock_user
    mock_session.delete.assert_called_once_with(mock_user)
    mock_session.commit.assert_called_once()


def test_delete_user_not_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(UserNotFoundException):
        delete_user(mock_session, str(uuid4()))
