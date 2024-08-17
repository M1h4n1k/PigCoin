from .utils import client, testing_user, get_client_with_dep, dummy_user
from orjson import dumps
from unittest.mock import Mock, AsyncMock, call, ANY, DEFAULT
import pytest
from copy import deepcopy


def test_parse_start_param():
    from routers.user import parse_start_param
    assert parse_start_param(None) == {}
    assert parse_start_param('2f') == {'userId': 0x2f, 'clubId': None}
    assert parse_start_param('1f_f1') == {'userId': 0x1f, 'clubId': -0xf1}


def test_user_login(mocker):
    patch_validate_data = mocker.patch('routers.user.validate_tg_data', Mock(return_value=True))

    response = client.post('/api/user/login', json=dumps(testing_user).decode())
    assert response.status_code == 200
    patch_validate_data.assert_called_once()


@pytest.mark.asyncio
async def test_user_login_create(mocker, dummy_user):
    patch_validate_data = mocker.patch('routers.user.validate_tg_data', Mock(return_value=True))
    mocker.patch('routers.user.crud.users.get_user', Mock(return_value=None))
    patch_bot_get_photos = mocker.patch('routers.user.bot.get_user_profile_photos', AsyncMock())
    patch_bot_get_photos.return_value = Mock(total_count=0)
    patch_crud_create_user = mocker.patch('routers.user.crud.users.create_user', Mock(return_value=dummy_user))

    response = client.post('/api/user/login', json=dumps(testing_user).decode())
    assert response.status_code == 200
    patch_bot_get_photos.assert_called_once()
    patch_crud_create_user.assert_called_once()
    patch_validate_data.assert_called_once()


@pytest.mark.asyncio
async def test_user_login_create_referral(mocker, dummy_user):
    def ret_user(db, tg_id):
        if tg_id == 1:
            return None
        ddummy_user = deepcopy(dummy_user)
        ddummy_user.tg_id = tg_id
        return ddummy_user
    patch_validate_data = mocker.patch('routers.user.validate_tg_data', Mock(return_value=True))
    mocker.patch('routers.user.crud.users.get_user', Mock(side_effect=ret_user))
    patch_bot_get_photos = mocker.patch('routers.user.bot.get_user_profile_photos', AsyncMock())
    patch_bot_get_photos.return_value = Mock(total_count=0)
    patch_crud_create_user = mocker.patch('routers.user.crud.users.create_user', Mock(return_value=dummy_user))
    patch_update_user_money = mocker.patch('routers.user.crud.users.update_user_money', Mock())
    patch_complete_task = mocker.patch('routers.user.crud.tasks.complete_task', Mock())

    testing_user_c = deepcopy(testing_user)
    testing_user_c['start_param'] = '1f'

    response = client.post('/api/user/login', json=dumps(testing_user_c).decode())
    assert response.status_code == 200
    patch_bot_get_photos.assert_called_once()
    patch_crud_create_user.assert_called_once()
    calls = patch_update_user_money.mock_calls
    assert len(calls) == 2
    assert calls[0].args[1].tg_id == 1
    assert calls[0].args[2] == 5000
    assert calls[1].args[1].tg_id == 0x1f
    assert calls[1].args[2] == 5000
    patch_complete_task.assert_called_once()
    assert patch_complete_task.mock_calls[0].args[1] == 3
    assert patch_complete_task.mock_calls[0].args[2] == 0x1f
    patch_validate_data.assert_called_once()


@pytest.mark.asyncio
async def test_user_login_create_referral_premium(mocker, dummy_user):
    def ret_user(db, tg_id):
        if tg_id == 1:
            return None
        ddummy_user = deepcopy(dummy_user)
        ddummy_user.tg_id = tg_id
        return ddummy_user
    patch_validate_data = mocker.patch('routers.user.validate_tg_data', Mock(return_value=True))
    mocker.patch('routers.user.crud.users.get_user', Mock(side_effect=ret_user))
    patch_bot_get_photos = mocker.patch('routers.user.bot.get_user_profile_photos', AsyncMock())
    patch_bot_get_photos.return_value = Mock(total_count=0)
    patch_crud_create_user = mocker.patch('routers.user.crud.users.create_user', Mock(return_value=dummy_user))
    patch_update_user_money = mocker.patch('routers.user.crud.users.update_user_money', Mock())
    patch_complete_task = mocker.patch('routers.user.crud.tasks.complete_task', Mock())

    testing_user_c = deepcopy(testing_user)
    testing_user_c['start_param'] = '1f'
    testing_user_c['user']['is_premium'] = True

    response = client.post('/api/user/login', json=dumps(testing_user_c).decode())
    assert response.status_code == 200
    patch_bot_get_photos.assert_called_once()
    patch_crud_create_user.assert_called_once()
    calls = patch_update_user_money.mock_calls
    assert len(calls) == 2
    assert calls[0].args[1].tg_id == 1
    assert calls[0].args[2] == 25000
    assert calls[1].args[1].tg_id == 0x1f
    assert calls[1].args[2] == 25000
    patch_complete_task.assert_called_once()
    assert patch_complete_task.mock_calls[0].args[1] == 3
    assert patch_complete_task.mock_calls[0].args[2] == 0x1f
    patch_validate_data.assert_called_once()


def test_user_referrals():
    def patch_get_user():
        return Mock(
            referrals=[],
            tg_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.get('/api/user/referrals')
    assert response.status_code == 200
