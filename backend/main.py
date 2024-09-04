import uvicorn
from routers import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.initialization import init
from contextlib import asynccontextmanager
import asyncio
from bot import dp, bot
import os
from bot.loader import WEB_LINK


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # asyncio.create_task(dp.start_polling(bot))
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
os.makedirs('photos', exist_ok=True)
app.mount('/api/photos', StaticFiles(directory='photos'), name='photos')
init()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000', 'http://84.249.17.76:3000', WEB_LINK],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


if __name__ == '__main__':
    uvicorn.run("main:app", port=3001, host='0.0.0.0', reload=True, forwarded_allow_ips='*')
