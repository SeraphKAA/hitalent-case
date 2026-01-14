from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import event, text
from typing import AsyncGenerator
import logging

from app.models import Base
from app.config import settings


logger = logging.getLogger(__name__)

# асинхронный движок для бд
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=getattr(settings, "DATABASE_ECHO", False),
    pool_size=getattr(settings, "DATABASE_POOL_SIZE", 20),
    max_overflow=getattr(settings, "DATABASE_MAX_OVERFLOW", 40),
    pool_pre_ping=getattr(settings, "DATABASE_POOL_PRE_PING", True),
    connect_args={"server_settings": {"jit": "off", "application_name": "fastapi_app"}},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения сессии базы данных
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Инициализация базы данных
    """
    try:
        # Создаем таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


async def check_db_connection():
    """
    Проверка подключения к базе данных
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


async def drop_db():
    """
    Удаление всех таблиц (только для тестов !!!)
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.warning("Database tables dropped")
