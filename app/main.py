from fastapi import FastAPI , Response
from app.DataBaseConfig.database import engine, Base
from app.routers import api_routers
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI()

app.include_router(api_routers.router)


@app.head("/", status_code=200)
def check_status():
    """
    Endpoint para verificacao do status da API (Health Check).
    """
    return Response()
