from fastapi import FastAPI
from api.router import router
from database import dbcontext
from contextlib import asynccontextmanager


# asynccontextmanager dekoriert die lifespan Funktion, damit sie als Kontextmanager verwendet werden kann.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await dbcontext.init_connection_db()
    yield
    await dbcontext.close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
