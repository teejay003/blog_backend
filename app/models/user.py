from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.post import post_likes

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # Admin flag
    is_superuser = Column(Boolean, default=False)  # Future use
    
    posts = relationship("Post", back_populates="author")
    liked_posts = relationship("Post", secondary=post_likes, back_populates="likes")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
