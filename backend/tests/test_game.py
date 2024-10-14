from unittest.mock import AsyncMock, Mock, ANY, call
import pytest
from .utils import client, dummy_user
from database.schemas import Club
from dependencies import get_user
from fastapi.testclient import TestClient


def get_client_with_dep(get_user_dep):
    app = client.app
    app.dependency_overrides[get_user] = get_user_dep
    return TestClient(app)


def test_collect_coins(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            click_price=35,
            current_energy=100,
            club_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_update_money = mocker.patch('routers.boosts.crud.users.update_user_money', Mock())
    dummy_user.club_id = 1
    patch_crud_update_money.return_value = dummy_user
    patch_crud_decrease_energy = mocker.patch('routers.boosts.crud.users.decrease_user_energy', Mock())
    patch_crud_update_cheated_count = mocker.patch('routers.boosts.crud.users.update_cheated_count', Mock())

    response = client_l.post('/api/game/collectCoins', json={'coins': 100})
    assert response.status_code == 200
    patch_crud_decrease_energy.assert_called_with(ANY, ANY, 100)
    patch_crud_update_cheated_count.assert_not_called()
    patch_crud_update_money.assert_called_with(ANY, ANY, 100)


def test_collect_coins_cheated(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            click_price=35,
            current_energy=10000,
            club_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_update_money = mocker.patch('routers.boosts.crud.users.update_user_money', Mock())
    dummy_user.club_id = 1
    patch_crud_update_money.return_value = dummy_user
    patch_crud_decrease_energy = mocker.patch('routers.boosts.crud.users.decrease_user_energy', Mock())
    patch_crud_update_cheated_count = mocker.patch('routers.boosts.crud.users.update_cheated_count', Mock())

    response = client_l.post('/api/game/collectCoins', json={'coins': 35 * 50})
    assert response.status_code == 200
    patch_crud_decrease_energy.assert_called_with(ANY, ANY, 35 * 50)
    patch_crud_update_cheated_count.assert_called_with(ANY, ANY, 1)
    patch_crud_update_money.assert_called_with(ANY, ANY, 35 * 50)


def test_collect_coins_negative(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            current_energy=100,
        )
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_update_money = mocker.patch('routers.boosts.crud.users.update_user_money', Mock())
    patch_crud_update_money.return_value = dummy_user
    patch_crud_decrease_energy = mocker.patch('routers.boosts.crud.users.decrease_user_energy', Mock())

    response = client_l.post('/api/game/collectCoins', json={'coins': -100})
    assert response.status_code == 400
    patch_crud_decrease_energy.assert_not_called()
    patch_crud_update_money.assert_not_called()


def test_collect_coins_low_energy(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            current_energy=0,
        )
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_update_money = mocker.patch('routers.boosts.crud.users.update_user_money', Mock())
    patch_crud_update_cheated_count = mocker.patch('routers.boosts.crud.users.update_cheated_count', Mock())
    patch_crud_update_money.return_value = dummy_user
    patch_crud_decrease_energy = mocker.patch('routers.boosts.crud.users.decrease_user_energy', Mock())

    response = client_l.post('/api/game/collectCoins', json={'coins': 100})
    assert response.status_code == 400
    patch_crud_decrease_energy.assert_not_called()
    patch_crud_update_cheated_count.assert_not_called()
    patch_crud_update_money.assert_not_called()


def test_get_turbo(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            turbo_available=True,
        )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.get('/api/game/turbo')
    assert response.status_code == 200
    assert response.json() is True


def test_get_turbo_false(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            turbo_available=False,
        )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.get('/api/game/turbo')
    assert response.status_code == 200
    assert response.json() is False


def test_collect_turbo(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            turbo_available=True,
            club_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_update_money = mocker.patch('routers.boosts.crud.users.update_user_money', Mock())
    patch_crud_decrease_energy = mocker.patch('routers.boosts.crud.users.decrease_user_energy', Mock())
    patch_crud_update_free_turbo = mocker.patch('routers.boosts.crud.users.update_user_turbo', Mock())
    dummy_user.club_id = 1
    patch_crud_update_free_turbo.return_value = dummy_user

    response = client_l.post('/api/game/collectTurboCoins', json={'coins': 100})
    assert response.status_code == 200
    patch_crud_decrease_energy.assert_not_called()
    patch_crud_update_money.assert_called_with(ANY, ANY, 100)
    patch_crud_update_free_turbo.assert_called_with(ANY, ANY, False)


def test_collect_turbo_unavailable(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            turbo_available=False,
            club_id=1,
        )

    client_l = get_client_with_dep(patch_get_user)
    patch_crud_update_money = mocker.patch('routers.boosts.crud.users.update_user_money', Mock())
    patch_crud_decrease_energy = mocker.patch('routers.boosts.crud.users.decrease_user_energy', Mock())
    patch_crud_update_free_turbo = mocker.patch('routers.boosts.crud.users.update_user_turbo', Mock())

    response = client_l.post('/api/game/collectTurboCoins', json={'coins': 100})
    assert response.status_code == 400
    patch_crud_decrease_energy.assert_not_called()
    patch_crud_update_money.assert_not_called()
    patch_crud_update_free_turbo.assert_not_called()


def test_collect_turbo_negative(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            turbo_available=True,
            club_id=1,
        )

    client_l = get_client_with_dep(patch_get_user)
    patch_crud_update_money = mocker.patch('routers.boosts.crud.users.update_user_money', Mock())
    patch_crud_decrease_energy = mocker.patch('routers.boosts.crud.users.decrease_user_energy', Mock())
    patch_crud_update_free_turbo = mocker.patch('routers.boosts.crud.users.update_user_turbo', Mock())

    response = client_l.post('/api/game/collectTurboCoins', json={'coins': -100})
    assert response.status_code == 400
    patch_crud_decrease_energy.assert_not_called()
    patch_crud_update_money.assert_not_called()
    patch_crud_update_free_turbo.assert_not_called()


def test_collect_turbo_cheated(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            turbo_available=True,
            club_id=1,
        )

    client_l = get_client_with_dep(patch_get_user)
    patch_crud_update_money = mocker.patch('routers.boosts.crud.users.update_user_money', Mock())
    patch_crud_decrease_energy = mocker.patch('routers.boosts.crud.users.decrease_user_energy', Mock())
    patch_crud_update_free_turbo = mocker.patch('routers.boosts.crud.users.update_user_turbo', Mock())
    patch_crud_update_cheated_count = mocker.patch('routers.boosts.crud.users.update_cheated_count', Mock())

    response = client_l.post('/api/game/collectTurboCoins', json={'coins': 2001})
    assert response.status_code == 400
    patch_crud_decrease_energy.assert_not_called()
    patch_crud_update_money.assert_not_called()
    patch_crud_update_free_turbo.assert_not_called()
    patch_crud_update_cheated_count.assert_called_with(ANY, ANY, 1)