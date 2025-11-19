from sqlalchemy import create_engine, func, Numeric, Integer, String, Float, Column, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

class Category(Base):
    __tablename__='categories'
    id = Column(Integer, primary_key=True, index = True) #indexed, but I think this will be plaid stuff
    name = Column(String, nullable = False)
    type = Column(String, nullable = False) #either income or expense
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable = False)

    ##RELATIONSHIPS: One category to many transactions. One categogory can have many budget goals
    transactions = relationship('Transaction', back_populates='category')
    goals = relationship('Budget', back_populates='category')