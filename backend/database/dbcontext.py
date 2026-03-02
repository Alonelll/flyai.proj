from database.models import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mac URL
DATABASE_URL = "postgresql+psycopg://ra7eem.@localhost:5432/fly_ai_db"
# windows URL
# DATABASE_URL = "postgresql+asyncpg://postgres:Test!1234@localhost:5433/fly_ai_db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_connection_db():
    try:
        async with engine.begin() as start_connection:
            # run_sync ermöglicht die Ausführung von synchronen Funktionen in einem asynchronen Kontext,
            # was hier notwendig ist, um die Metadaten der Datenbank zu erstellen.
            await start_connection.run_sync(Base.metadata.create_all)
        logger.info("Database connection and initialization successful.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")


async def close_db():
    await engine.dispose()
