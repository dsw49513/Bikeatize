from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+asyncmy://root:bikeatize2001$%%@localhost/bikeatize_db"

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
