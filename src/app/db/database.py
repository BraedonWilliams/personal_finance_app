from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This is where you'll put the enginge, SessionLocal, Base, Get_db() ... #

engine = create_engine('postgresql+psycopg2://braedon:pfinbw@localhost/personal_finance', echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
