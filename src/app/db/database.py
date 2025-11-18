from sqlalchemy import create_engine, Integer, String, Float, Column, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# This is where you'll put the enginge, SessionLocal, Base, Get_db() ... #

# Create the engine (think doorway to the house) ...session is the room, the objects/tables are
# the furniture in the room that is actually acted on
engine = create_engine('postgresql+psycopg2://braedon:pfinbw@localhost/personal_finance
', echo=True)

Base = declarative_base

#define a table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, nullable = False, unique = True)
    password_hash = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable = False)

