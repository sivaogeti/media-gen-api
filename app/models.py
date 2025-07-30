from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MediaGeneration(Base):
    __tablename__ = "media_generations"

    id = Column(Integer, primary_key=True, index=True)
    media_type = Column(String)
    prompt = Column(String)
    file_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
