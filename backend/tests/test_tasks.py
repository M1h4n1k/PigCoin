from .utils import client, get_client_with_dep
from unittest.mock import Mock


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

