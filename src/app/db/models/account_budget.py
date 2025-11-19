from sqlalchemy import create_engine, func, Numeric, Integer, String, Float, Column, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

class AccountBudget(Base):
    __tablename__ = 'account_budgets'

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    budget_id = Column(Integer, ForeignKey('budgets.id'), nullable=False)

    current_progress = Column(Float, nullable=False, default=0)

    # Relationships
    account = relationship('Account', back_populates='budget_links')
    budget = relationship('Budget', back_populates='account_links')