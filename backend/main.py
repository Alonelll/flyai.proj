from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
