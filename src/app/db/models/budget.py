from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    period = Column(String, nullable=False)  # "monthly", "weekly", "yearly", etc.

    # Owner + category this budget tracks
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # 🔥 Progress tracking
    current_spent = Column(Float, nullable=False, default=0.0)
    remaining = Column(Float, nullable=False, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # relationships
    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="goals")
    account_links = relationship("AccountBudget", back_populates="budget")
