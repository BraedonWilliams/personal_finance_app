from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.app.db.database import Base


class PlaidItem(Base):
    __tablename__ = "plaid_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    access_token = Column(String, nullable=False)
    item_id = Column(String, nullable=False)
    institution_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="plaid_items")
    accounts = relationship("BankAccount", back_populates="plaid_item")

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    plaid_account_id = Column(String, unique=True)
    name = Column(String)
    official_name = Column(String)
    type = Column(String)
    subtype = Column(String)
    mask = Column(String)

    current_balance = Column(Integer)
    available_balance = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("plaid_items.id"))

    user = relationship("User", back_populates="bank_accounts")
    plaid_item = relationship("PlaidItem", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    plaid_transaction_id = Column(String, unique=True, index=True)
    
    name = Column(String)
    date = Column(String)
    amount = Column(Integer)

    category = Column(String)   # Store as comma-separated at first
    pending = Column(Integer)

    account_id = Column(Integer, ForeignKey("bank_accounts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    account = relationship("BankAccount", back_populates="transactions")
    user = relationship("User", back_populates="transactions")

plaid_items = relationship("PlaidItem", back_populates="user")
bank_accounts = relationship("BankAccount", back_populates="user")
transactions = relationship("Transaction", back_populates="user")
