from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from db_conn import Base, engine_newsletter, metadata
from config import DATABASE_URI


# ---------------- Criacao de Entidades e Agregados (DDD) ----------------
class User(Base):
    
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    frequency = Column(String, nullable=False)

class EmailLog(Base):
    __tablename__ = 'email_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# ---------------- Insersão no PostgreSQL ----------------
Base.metadata.create_all(bind=engine_newsletter)

