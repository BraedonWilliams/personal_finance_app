from sqlalchemy import create_engine, func, Numeric, Integer, String, Float, Column, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from ..database import Base

class Transaction(Base):
    __tablename__= 'transactions'
    id = Column(Integer, primary_key = True) #to index or not to index
    amount = Column(Numeric(12, 2), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = Column(String, nullable=True) #nullable should be fine
    type = Column(String, nullable=False)
    notes = Column(String, nullable = True)

    #Foreign Keys
    account_id = Column(Integer, ForeignKey('accounts.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    # Relationships: belongs to one account and belongs to one category
    account = relationship('Account', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')