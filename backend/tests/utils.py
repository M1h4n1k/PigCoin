import bot
from fastapi.testclient import TestClient
import json
from sqlalchemy.orm import Session
from main import app
from database import crud, models, schemas
from database.loader import SessionLocal
from dependencies import get_user

from aiogram import types
from hashlib import sha256
import hmac

import pytest
from unittest.mock import Mock
from copy import deepcopy, copy


def get_client_with_dep(get_user_dep):
    app_ = client.app
    app_.dependency_overrides[get_user] = get_user_dep
    return TestClient(app_)


@pytest.fixture(scope='function')
def dummy_user():
    return Mock(
        picture='test',         username='test',  total_coins=0,  current_energy=0,       max_energy=0,
        turbo_available=False,  click_price=0,    refill_rate=0,  league=0,               free_turbo=0,
        free_refills=0,         club_id=None,     club=None,      position_in_club=None,  position=None,
        current_coins=300,      boosts=[],        tg_id=1,        can_collect_ad=False,
    )


def create_hash(data):
    secret_key = hmac.new(b'WebAppData', msg=bot.TOKEN.replace('/test', '').encode(), digestmod=sha256).digest()
    payload = f"auth_date={data['auth_date']}\n" \
              f"query_id={data['query_id']}\n" \
              f"user={json.dumps(data['user'], separators=(',', ':'))}"
    hashed_data = hmac.new(secret_key, msg=payload.encode(), digestmod=sha256).hexdigest()
    return hashed_data


testing_user = {
    'query_id': 'AAGlqEg-AAAAAKWoSD7eUaLE',
    'user': {
        'id': 1,
        'first_name': 'User',
        'last_name': 'Testing',
        'username': 'tuser',
        'language_code': 'ru'
    },
    'auth_date': '1674072736',
}

testing_user['hash'] = create_hash(testing_user)

client = TestClient(app, cookies={'tg_data': json.dumps(testing_user)})

db = SessionLocal()
if crud.users.get_user(db, 1) is None:
    crud.users.create_user(db, schemas.UserCreate(
        tg_id=1,
        username='User Testing',
        picture='https://example.com/picture.jpg',
        referrer_tg_id=None,
        club_id=None
    ))
db.close()
