from unittest.mock import AsyncMock, Mock, ANY
import pytest
from .utils import client, get_client_with_dep, dummy_user
from database.schemas import Club


def test_create_join_club(mocker, dummy_user):
    def patch_get_user():
        dummy_user.club_id = None
        return dummy_user
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_club_get = mocker.patch('routers.clubs.crud.clubs.get_club_by_name', Mock())
    patch_crud_club_get.return_value = Mock(id=1)
    patch_crud_user = mocker.patch('routers.clubs.crud.users.update_user_club', Mock())

    response = client_l.post('/api/clubs/', json='test')
    assert response.status_code == 201
    assert patch_crud_club_get.called
    patch_crud_user.assert_called_with(ANY, ANY, 1)


@pytest.mark.asyncio
async def test_create_club(mocker):
    patch_crud_club_get = mocker.patch('routers.clubs.crud.clubs.get_club_by_name', Mock(return_value=None))
    patch_crud_user = mocker.patch('routers.clubs.crud.users.update_user_club', Mock(return_value=None))
    patch_crud_club_create = mocker.patch('routers.clubs.crud.clubs.create_club', Mock(return_value=Mock(id=1)))
    patch_bot_get_chat = mocker.patch('routers.clubs.bot.get_chat', AsyncMock(return_value=Mock(photo=None)))

    response = client.post('/api/clubs/', json='test')
    assert response.status_code == 201
    assert patch_crud_club_get.called
    patch_crud_user.assert_called_with(ANY, ANY, 1)
    patch_crud_club_create.assert_called_with(ANY, ANY)
    patch_bot_get_chat.assert_called_with('@test')


def test_join_club(mocker):
    patch_crud_club_get = mocker.patch('routers.clubs.crud.clubs.get_club', Mock())
    patch_crud_club_get.return_value = Club(
        id=1,
        name='test',
        picture='test',
        tg_tag='test',
        total_coins=0,
        league=1,
        members_count=0,
    )
    patch_crud_user = mocker.patch('routers.clubs.crud.users.update_user_club', Mock(return_value=None))

    response = client.post('/api/clubs/1/join')
    assert response.status_code == 200
    assert patch_crud_club_get.called
    patch_crud_user.assert_called_with(ANY, ANY, 1)
