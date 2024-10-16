from copy import deepcopy

from .utils import get_client_with_dep, dummy_user, client
from unittest.mock import Mock, call, ANY
from datetime import datetime, timedelta


def patch_get_user_auc():
    return Mock(tg_id=1, uid='123', picture='test', username='test', total_coins=50000, current_coins=50000)


decoration_mock_ = Mock(
    id=1,
    title='crown',
    picture='/crown.png',
    initial_price=1000,
    last_bet=1000,
    last_bet_user=None,
    type='user',
    betting_ends_at=datetime.now() + timedelta(days=1),
)


def test_bet(mocker, dummy_user):
    decoration_mock = deepcopy(decoration_mock_)
    get_decoration_patch = mocker.patch('routers.user.crud.decorations.get_decoration_by_id', Mock(return_value=decoration_mock))
    make_decoration_patch = mocker.patch('routers.user.crud.decorations.make_bet', Mock(return_value=decoration_mock))

    client_l = get_client_with_dep(patch_get_user_auc)
    response = client_l.post('/api/decorations/bet', json={'decoration_id': decoration_mock.id, 'amount': 10000})
    assert response.status_code == 200
    assert get_decoration_patch.mock_calls == [call(ANY, decoration_mock.id)]
    assert make_decoration_patch.mock_calls == [call(ANY, ANY, decoration_mock, 10000)]


def test_bet_ended(mocker, dummy_user):
    decoration_mock = deepcopy(decoration_mock_)
    decoration_mock.betting_ends_at = datetime.now() - timedelta(days=1)
    get_decoration_patch = mocker.patch('routers.user.crud.decorations.get_decoration_by_id', Mock(return_value=decoration_mock))
    make_decoration_patch = mocker.patch('routers.user.crud.decorations.make_bet', Mock(return_value=decoration_mock))

    client_l = get_client_with_dep(patch_get_user_auc)
    response = client_l.post('/api/decorations/bet', json={'decoration_id': decoration_mock.id, 'amount': 10000})
    assert response.status_code == 403
    assert get_decoration_patch.mock_calls == [call(ANY, decoration_mock.id)]
    assert make_decoration_patch.mock_calls == []


def test_bet_not_enough_coins(mocker, dummy_user):
    decoration_mock = deepcopy(decoration_mock_)
    get_decoration_patch = mocker.patch('routers.user.crud.decorations.get_decoration_by_id', Mock(return_value=decoration_mock))
    make_decoration_patch = mocker.patch('routers.user.crud.decorations.make_bet', Mock(return_value=decoration_mock))

    client_l = get_client_with_dep(patch_get_user_auc)
    response = client_l.post('/api/decorations/bet', json={'decoration_id': decoration_mock.id, 'amount': 100000})
    assert response.status_code == 412
    assert get_decoration_patch.mock_calls == [call(ANY, decoration_mock.id)]
    assert make_decoration_patch.mock_calls == []


def test_bet_lower_bet(mocker, dummy_user):
    decoration_mock = deepcopy(decoration_mock_)
    decoration_mock.last_bet = 10000
    get_decoration_patch = mocker.patch('routers.user.crud.decorations.get_decoration_by_id', Mock(return_value=decoration_mock))
    make_decoration_patch = mocker.patch('routers.user.crud.decorations.make_bet', Mock(return_value=decoration_mock))

    client_l = get_client_with_dep(patch_get_user_auc)
    response = client_l.post('/api/decorations/bet', json={'decoration_id': decoration_mock.id, 'amount': 10000})
    assert response.status_code == 406
    assert get_decoration_patch.mock_calls == [call(ANY, decoration_mock.id)]
    assert make_decoration_patch.mock_calls == []


def test_get_auction(mocker, dummy_user):
    decoration_mock = deepcopy(decoration_mock_)
    get_decoration_patch = mocker.patch('routers.user.crud.decorations.get_decoration_on_auction', Mock(return_value=decoration_mock))

    response = client.get('/api/decorations/')
    assert response.status_code == 200
    get_decoration_patch.assert_called_once()
