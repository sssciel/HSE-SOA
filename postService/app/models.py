from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ARRAY
from sqlalchemy.sql import func
from database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creator_id = Column(Integer, nullable=False)
    is_private = Column(Boolean, default=False)
    tags = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())