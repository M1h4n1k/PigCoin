from .utils import client, testing_user, get_client_with_dep
from orjson import dumps
from unittest.mock import Mock


def test_parse_start_param():
    from routers.user import parse_start_param
    assert parse_start_param(None) == {}
    assert parse_start_param('2f') == {'userId': 0x2f, 'clubId': None}
    assert parse_start_param('1f_f1') == {'userId': 0x1f, 'clubId': -0xf1}


def test_user_login():
    response = client.post('/api/user/login', json=dumps(testing_user).decode())
    assert response.status_code == 200


def test_user_referrals():
    def patch_get_user():
        return Mock(
            referrals=[],
            tg_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.get('/api/user/referrals')
    assert response.status_code == 200
