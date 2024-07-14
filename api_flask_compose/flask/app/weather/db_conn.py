from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URI

# ---------------- Objetos para comunicação com o PostgreSQL ----------------
engine_weather = create_engine(DATABASE_URI)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine_weather)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

