import uvicorn
from routers import router
from fastapi import FastAPI
from database import models
from database.loader import engine

app = FastAPI()
app.include_router(router)

models.Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    uvicorn.run("main:app", port=84, host='0.0.0.0', reload=True, forwarded_allow_ips='*')
