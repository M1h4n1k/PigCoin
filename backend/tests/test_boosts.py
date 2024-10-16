from unittest.mock import AsyncMock, Mock, ANY
from .utils import dummy_user, get_client_with_dep


def test_get_boosts(dummy_user):
    client_l = get_client_with_dep(lambda : dummy_user)
    response = client_l.get('/api/boosts/')
    assert response.status_code == 200
    assert sorted(response.json(), key=lambda r: r['id']) == response.json()


def test_buy_boost(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            current_coins=300,
            boosts=[],
            tg_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_boost_get = mocker.patch('routers.boosts.crud.boosts.get_boost', Mock())
    patch_crud_boost_get.return_value = Mock(base_price=100, type='test')
    patch_crud_user = mocker.patch('routers.boosts.crud.users.update_user_money', Mock(return_value=dummy_user))
    patch_crud_boost_buy = mocker.patch('routers.boosts.crud.boosts.buy_boost', Mock(return_value=None))

    response = client_l.post('/api/boosts/buy/1')
    assert response.status_code == 200
    assert patch_crud_boost_get.called
    patch_crud_user.assert_called_with(ANY, ANY, -100)
    patch_crud_boost_buy.assert_called_with(ANY, ANY, 1, 'test')


def test_buy_boost_fail(mocker, dummy_user):
    def patch_get_user():
        return Mock(
            current_coins=0,
            boosts=[],
            tg_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_boost_get = mocker.patch('routers.boosts.crud.boosts.get_boost', Mock())
    patch_crud_boost_get.return_value = Mock(base_price=100, type='test')
    patch_crud_user = mocker.patch('routers.boosts.crud.users.update_user_money', Mock(return_value=dummy_user))
    patch_crud_boost_buy = mocker.patch('routers.boosts.crud.boosts.buy_boost', Mock(return_value=None))

    response = client_l.post('/api/boosts/buy/1')
    assert response.status_code == 402
    assert patch_crud_boost_get.called
    assert not patch_crud_user.called
    assert not patch_crud_boost_buy.called


def test_use_turbo(mocker, dummy_user):
    def patch_get_user():
        return Mock(free_turbo=1)
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_user = mocker.patch('routers.boosts.crud.users.user_use_free_turbo', Mock(return_value=dummy_user))

    response = client_l.post('/api/boosts/use/0')
    assert response.status_code == 200
    patch_crud_user.assert_called_with(ANY, ANY)


def test_use_turbo_fail():
    def patch_get_user():
        return Mock(free_turbo=0)
    client_l = get_client_with_dep(patch_get_user)

    response = client_l.post('/api/boosts/use/0')
    assert response.status_code == 400


def test_use_refill(mocker, dummy_user):
    def patch_get_user():
        return Mock(free_refills=1)
    client_l = get_client_with_dep(patch_get_user)
    patch_crud_user = mocker.patch('routers.boosts.crud.users.user_use_free_refill', Mock(return_value=dummy_user))

    response = client_l.post('/api/boosts/use/1')
    assert response.status_code == 200
    patch_crud_user.assert_called_with(ANY, ANY)


def test_use_refill_fail():
    def patch_get_user():
        return Mock(free_refills=0)
    client_l = get_client_with_dep(patch_get_user)

    response = client_l.post('/api/boosts/use/1')
    assert response.status_code == 400
