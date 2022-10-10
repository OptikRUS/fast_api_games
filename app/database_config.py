from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://admin:password123456@postgres_db:5432/games_db"

Base = declarative_base()

# Make the engine
engine = create_async_engine(DATABASE_URL,
                             future=True,
                             # echo=True,  # echo включает ведение лога через стандартный модуль logging
                             )
# create async session
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
