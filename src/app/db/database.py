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


# IMPORT ALL MODELS HERE
from src.app.db.models import (
    account,
    category,
    budget,
    transaction,
    account_budget
)

Base.metadata.create_all(bind=engine)
