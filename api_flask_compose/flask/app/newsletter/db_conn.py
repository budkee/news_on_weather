from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URI

# ---------------- Objetos para comunicação com o PostgreSQL ----------------
engine_newsletter = create_engine(DATABASE_URI)
Session = sessionmaker(autocommit=False, autoflush=False,bind=engine_newsletter)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


