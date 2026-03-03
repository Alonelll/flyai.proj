from fastapi import FastAPI
from backend.api.router_controller import router
from contextlib import asynccontextmanager
from backend.database import dbcontext


# asynccontextmanager dekoriert die lifespan Funktion, damit sie als Kontextmanager verwendet werden kann.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await dbcontext.init_connection_db()
    yield
    await dbcontext.close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
