from sqlalchemy import (
    Column, Integer, Numeric, String, Date, Boolean, ForeignKey, DateTime, func
)
from sqlalchemy.orm import relationship
from ..database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Numeric(12, 2), nullable=False)

    # MATCHES schema: `date: dt_date`
    date = Column(Date, nullable=False)

    description = Column(String, nullable=True)

    # MATCHES schema: `is_income: bool`
    is_income = Column(Boolean, nullable=False, default=False)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Auto timestamp (optional)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
