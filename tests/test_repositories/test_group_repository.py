import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.repository.group import (
    create_group,
    get_group,
    get_groups,
    update_group,
    delete_group,
)
from app.exceptions.group_not_found_exception import GroupNotFoundException
from app.models.group import Group
from app.schemas.group import GroupCreate


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_group():
    return Group(uuid=str(uuid4()), name="Test Group")


def test_create_group(mock_session):
    group_data = GroupCreate(name="New Group")
    mock_group_instance = Group(uuid=str(uuid4()), name=group_data.name)

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda group: setattr(
        group, "uuid", mock_group_instance.uuid
    )

    created_group = create_group(mock_session, group_data)

    assert created_group.name == "New Group"
    assert created_group.uuid == mock_group_instance.uuid
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(created_group)


def test_get_group_success(mock_session, mock_group):

    mock_session.query.return_value.filter.return_value.first.return_value = mock_group

    group = get_group(mock_session, mock_group.uuid)

    assert group.uuid == mock_group.uuid
    assert group.name == mock_group.name
    mock_session.query.return_value.filter.return_value.first.assert_called_once()


def test_get_group_not_found(mock_session):

    mock_session.query.return_value.filter.return_value.first.return_value = None
    non_existent_uuid = str(uuid4())

    with pytest.raises(GroupNotFoundException) as exc:
        get_group(mock_session, non_existent_uuid)

    assert f"Group with the id {non_existent_uuid}" in str(exc.value)


def test_get_groups(mock_session, mock_group):

    mock_session.query.return_value.all.return_value = [mock_group]

    groups = get_groups(mock_session)

    assert len(groups) == 1
    assert groups[0].uuid == mock_group.uuid
    assert groups[0].name == mock_group.name
    mock_session.query.return_value.all.assert_called_once()


def test_update_group_success(mock_session, mock_group):

    mock_session.query.return_value.filter.return_value.first.return_value = mock_group
    updated_data = {"name": "Updated Group"}

    updated_group = update_group(mock_session, mock_group.uuid, updated_data)

    assert updated_group.name == "Updated Group"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(updated_group)


def test_update_group_not_found(mock_session):

    mock_session.query.return_value.filter.return_value.first.return_value = None
    non_existent_uuid = str(uuid4())
    updated_data = {"name": "Updated Group"}

    with pytest.raises(GroupNotFoundException) as exc:
        update_group(mock_session, non_existent_uuid, updated_data)

    assert f"Group with the id {non_existent_uuid}" in str(exc.value)


def test_delete_group_success(mock_session, mock_group):

    mock_session.query.return_value.filter.return_value.first.return_value = mock_group

    deleted_group = delete_group(mock_session, mock_group.uuid)

    assert deleted_group.uuid == mock_group.uuid
    mock_session.delete.assert_called_once_with(mock_group)
    mock_session.commit.assert_called_once()


def test_delete_group_not_found(mock_session):

    mock_session.query.return_value.filter.return_value.first.return_value = None
    non_existent_uuid = str(uuid4())

    with pytest.raises(GroupNotFoundException) as exc:
        delete_group(mock_session, non_existent_uuid)

    assert f"Group with the id {non_existent_uuid}" in str(exc.value)
