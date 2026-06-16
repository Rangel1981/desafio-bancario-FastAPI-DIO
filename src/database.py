from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# URL de Conexão: driver://user:password@host:port/dbname
# Importante: postgresql+asyncpg para ser assíncrono
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user_api:password_api@localhost:5432/banking_db"

# criando engine assicrono
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# session
SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()