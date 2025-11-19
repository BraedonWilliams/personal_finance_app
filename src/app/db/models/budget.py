from sqlalchemy import create_engine, func, Numeric, Integer, String, Float, Column, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

class Budget(Base): #for budget goals
    __tablename__='budgets'    
    id = Column(Integer, primary_key=True, nullable = False, index = True)
    name = Column(String, nullable = False)
    target_amnt = Column(Numeric(12, 2), nullable = False)
    start_date = Column(Date, nullable = False)
    end_date = Column(Date, nullable = False)
    is_complete = Column(Boolean, nullable = False)

    #Foreign Keys
    category_id=Column(Integer, ForeignKey('categories.id'))

    #Relationships
    category = relationship('Category', back_populates='goals')
    account_links = relationship('AccountBudget', back_populates='budget')
