from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, inspect, text
from sqlalchemy.orm import relationship
from db_conn import Base, engine_newsletter, metadata
from config import DATABASE_URI


# ---------------- Criacao de Entidades e Agregados (DDD) ----------------
class User(Base):
    
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    frequency = Column(String, nullable=False)

    # Relationship to EmailLog
    email_logs = relationship("EmailLog", back_populates="user")


class EmailLog(Base):
    __tablename__ = 'email_logs'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

     # Foreign Key to link EmailLog with User
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship to User
    user = relationship("User", back_populates="email_logs")
# ---------------- Insersão no PostgreSQL ----------------


# Acquire an advisory lock (arbitrary number as lock identifier, e.g., 12345)
with engine_newsletter.connect() as connection:
    connection.execute(text("SELECT pg_advisory_lock(12345)"))
    
    try:
        # Check and create the table within the lock
        inspector = inspect(engine_newsletter)

        if not inspector.has_table('users') or not inspector.has_table('email_logs'):
            Base.metadata.create_all(bind=engine_newsletter)
    finally:
        # Release the advisory lock
        connection.execute(text("SELECT pg_advisory_unlock(12345)"))