import uvicorn
from routers import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import models
from database.loader import engine
from contextlib import asynccontextmanager
import asyncio
from bot import dp, bot
import os

@asynccontextmanager
async def lifespan(_app: FastAPI):
    asyncio.create_task(dp.start_polling(bot))
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
os.makedirs('photos', exist_ok=True)
app.mount('/api/photos', StaticFiles(directory='photos'), name='photos')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5173', 'http://84.249.17.76:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

models.Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    uvicorn.run("main:app", port=84, host='0.0.0.0', reload=True, forwarded_allow_ips='*')
