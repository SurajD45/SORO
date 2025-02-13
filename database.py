from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatHistory(Base):
    _tablename_ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    chatbot_response = Column(String, nullable=False)
    sentiment = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DiaryEntry(Base):
    _tablename_ = "diary_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    entry = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)