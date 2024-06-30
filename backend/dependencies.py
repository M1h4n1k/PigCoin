from database.loader import SessionLocal
from database import crud, models
from fastapi import Request, HTTPException, Depends
from hashlib import sha256
import hmac
import orjson
from bot import TOKEN


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_tg_data(tg_data: str) -> bool:
    secret_key = hmac.new(b'WebAppData', msg=TOKEN.replace('/test', '').encode(), digestmod=sha256).digest()
    if not tg_data:
        return False
    tg_data = orjson.loads(tg_data)
    if 'user' not in tg_data:
        return False
    user_data = orjson.dumps(tg_data['user']).decode().replace('/', '\\/')
    tg_data['user'] = user_data
    sorted_items = sorted(tg_data.items())
    payload = '\n'.join([f'{key}={value}' for key, value in sorted_items if key != 'hash'])
    hashed_data = hmac.new(secret_key, msg=payload.encode(), digestmod=sha256).hexdigest()
    if tg_data['hash'] != hashed_data:
        print('Invalid hash', tg_data['hash'], hashed_data)
    return hashed_data == tg_data['hash']


async def get_tg_data(request: Request) -> dict:
    if not request.cookies.get('tg_data'):
        raise HTTPException(status_code=400, detail='No tg_data')
    if not validate_tg_data(request.cookies.get('tg_data')):
        raise HTTPException(status_code=400, detail='Invalid hash')
    return orjson.loads(request.cookies.get('tg_data'))


async def get_user(tg_data: dict = Depends(get_tg_data), db=Depends(get_db)) -> models.User:
    user = crud.users.get_user(db, tg_data['user']['id'])
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
