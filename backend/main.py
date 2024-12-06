from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from bot.loader import WEB_LINK
from database.initialization import init
from database.loader import scheduler
from routers import router
import logging


@asynccontextmanager
async def lifespan(_app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
os.makedirs('photos', exist_ok=True)
app.mount('/api/photos', StaticFiles(directory='photos'), name='photos')
init()


@app.middleware("http")
async def verify_headers(request: Request, call_next):
    headers = request.headers.get('User-Agent', '').lower()
    if 'mozilla' not in headers and 'chrome' not in headers and 'apple' not in headers:
        logging.warning(f'Cheating detected: {request.url} | {request.headers.get("User-Agent")} | {request.cookies.get("tg_data")}')
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000', WEB_LINK],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


if __name__ == '__main__':
    uvicorn.run("main:app", port=3001, host='0.0.0.0', reload=False, forwarded_allow_ips='*')
