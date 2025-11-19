from sqlalchemy import create_engine, func, Integer, String, Column, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, nullable = False, unique = True)
    password_hash = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable = False)

    #Relationships: one user has many accounts
    accounts = relationship('Account', back_populates='user')
