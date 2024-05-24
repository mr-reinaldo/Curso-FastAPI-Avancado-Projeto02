from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.core.settings import settings


# Criando a engine de conexão com o banco de dados
engine = create_engine(
    url=settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    echo_pool=settings.DATABASE_ECHO_POOL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)

# Criando a sessão de conexão com o banco de dados
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)
