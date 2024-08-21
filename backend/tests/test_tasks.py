from .utils import client, get_client_with_dep
from unittest.mock import Mock, ANY
from .utils import dummy_user


def test_get_tasks():
    def patch_get_user():
        return Mock(
            tasks_completed=[],
            tg_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.get('/api/tasks')
    assert response.status_code == 200


def test_get_tasks_completed():
    def patch_get_user():
        return Mock(
            tasks_completed=[Mock(id=1)],
            tg_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.get('/api/tasks')
    assert response.status_code == 200
    assert response.json()[0]['completed']


def test_watch_ad(mocker, dummy_user):
    patch_crud_watch_ad = mocker.patch('routers.boosts.crud.tasks.watch_ad', Mock(return_value=dummy_user))

    def patch_get_user():
        return Mock(
            tg_id=1,
            club_id=None,
            can_collect_ad=True,
        )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.post('/api/tasks/ad')
    assert response.status_code == 200
    patch_crud_watch_ad.assert_called_with(ANY, 1)


def test_watch_ad_fail():
    def patch_get_user():
        return Mock(
            can_collect_ad=False,
            tg_id=1,
        )
    client_l = get_client_with_dep(patch_get_user)
    response = client_l.post('/api/tasks/ad')
    assert response.status_code == 425
