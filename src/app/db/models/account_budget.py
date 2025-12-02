from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class AccountBudget(Base):
    __tablename__ = "account_budgets"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)

    current_progress = Column(Float, nullable=False, default=0.0)

    account = relationship("Account", back_populates="account_budgets")
    budget = relationship("Budget", back_populates="account_budgets")
