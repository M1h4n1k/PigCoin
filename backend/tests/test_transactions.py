from .utils import get_client_with_dep, dummy_user
from unittest.mock import Mock, call, ANY


def test_make_transaction(mocker, dummy_user):
    def patch_get_user():
        return Mock(tg_id=1, uid='123', picture='test', username='test', total_coins=500, current_coins=500)
    get_user_patch = mocker.patch('routers.user.crud.users.get_user_by_uid', Mock(return_value=dummy_user))
    make_transaction_patch = mocker.patch(
        'routers.user.crud.users.make_transaction',
        Mock(return_value={
            'amount': 100,
            'from_user': patch_get_user(),
            'to_user': dummy_user,
            'created_at': '2022-12-12T12:12:12'
        })
    )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.post('/api/transactions', json={'to_user_uid': dummy_user.uid, 'amount': 100})
    assert response.status_code == 200
    assert get_user_patch.mock_calls == [call(ANY, dummy_user.uid)]
    assert make_transaction_patch.mock_calls == [call(ANY, ANY, dummy_user, 100)]


def test_make_transaction_no_coins(mocker, dummy_user):
    def patch_get_user():
        return Mock(tg_id=1, uid='123', picture='test', username='test', total_coins=500, current_coins=500)
    mocker.patch('routers.user.crud.users.get_user_by_uid', Mock(return_value=dummy_user))
    make_transaction_patch = mocker.patch('routers.user.crud.users.make_transaction')
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.post('/api/transactions', json={'to_user_uid': dummy_user.uid, 'amount': 1000})
    assert response.status_code == 402
    assert make_transaction_patch.mock_calls == []


def test_make_transaction_user_not_found(mocker, dummy_user):
    def patch_get_user():
        return Mock(tg_id=1, uid=123, picture='test', username='test', total_coins=500, current_coins=500)
    mocker.patch('routers.user.crud.users.get_user_by_uid', Mock(return_value=None))
    make_transaction_patch = mocker.patch('routers.user.crud.users.make_transaction')
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.post('/api/transactions', json={'to_user_uid': dummy_user.uid, 'amount': 100})
    assert response.status_code == 404
    assert make_transaction_patch.mock_calls == []


def test_make_transaction_to_self(mocker):
    def patch_get_user():
        return Mock(tg_id=1, uid='123', picture='test', username='test', total_coins=500, current_coins=500)
    mocker.patch('routers.user.crud.users.get_user_by_uid', Mock(return_value=None))
    make_transaction_patch = mocker.patch('routers.user.crud.users.make_transaction')
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.post('/api/transactions', json={'to_user_uid': '123', 'amount': 100})
    assert response.status_code == 400
    assert make_transaction_patch.mock_calls == []
