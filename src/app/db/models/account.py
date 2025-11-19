from sqlalchemy import create_engine, func, Numeric, Integer, String, Float, Column, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key = True, index = True) #should get from plaid I think ?
    name = Column(String, nullable = False)
    type = Column(String, nullable = False)
    start_bal = Column(Integer, nullable = False)
    current_bal = Column(Integer, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default=func.now(), nullable = False)

    # Foreign Keys:
    user_id = Column(Integer, ForeignKey('users.id'))

    #Relationships: one account, many transactions...Many acct, many budget goals via join table
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')
    budget_links = relationship('AccountBudget', back_populates='account')
    
