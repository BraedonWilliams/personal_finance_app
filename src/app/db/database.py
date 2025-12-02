from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    'postgresql+psycopg2://braedon:pfinbw@localhost/personal_finance',
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# IMPORTANT: Import ALL models here
from src.app.db.models import User, Account, Category, Budget, Transaction, AccountBudget

Base.metadata.create_all(bind=engine)
