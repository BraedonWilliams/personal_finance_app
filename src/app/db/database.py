from sqlalchemy import create_engine, func, Integer, String, Float, Column, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# This is where you'll put the enginge, SessionLocal, Base, Get_db() ... #

# Create the engine (think doorway to the house) ...session is the room, the objects/tables are
# the furniture in the room that is actually acted on
engine = create_engine('postgresql+psycopg2://braedon:pfinbw@localhost/personal_finance', echo=True)

Base = declarative_base()

#define a table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, nullable = False, unique = True)
    password_hash = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable = False)

    #Relationships: one user has many accounts
    accounts = relationship('Account', back_populates='user')

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key = True, index = False) #should get from plaid I think ?
    name = Column(String, nullable = False)
    type = Column(String, nullable = False)
    start_bal = Column(Integer, nullable = False)
    current_bal = Column(Integer, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default=func.now(), nullable = False)

    # Foreign Keys:
    owner = Column(Integer, ForeignKey('users.id'))

    #Relationships: one account, many transactions...One acct, many budget goals via join table
    user = relationship('User', back_populates='accounts')
    
""" 
class Transaction(Base):
    __tablename__= 'transactions'
    id = Column(Integer, primary_key = True) #to index or not to index
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=false)
    description = Column(String, nullable=True) #nullable should be fine
    type = Column(String, nullable=False)
    notes = Column(String, nullable = True)

    # Relationships: belongs to one account and belongs to one category

class Category(Base):
    __tablename__='categories'
    id = Column(Integer, primary_key=True, index = True) #indexed, but I think this will be plaid stuff
    name = Column(String, nullable = False)
    type = Column(String, nullable = False) #either income or expense
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable = False)

    ##RELATIONSHIPS: One category to many transactions. One category to one budget goal


class Budget(Base): #for budget goals
    __tablename__='budgets'    
    id = Column(Integer, primary_key=True, nullable = False, index = True)
    name = Column(String, nullable = False)
    target_amnt = Column(Integer, nullable = False)
    start_date = Column(Date, nullable = False)
    end_date = Column(Date, nullable = False)
    is_complete = Column(Boolean, nullable = False)

 """

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session() #creates an instance of this session

new_user = User(username='firstUser', password_hash='password', email='firstUser@gmail.com')
session.add(new_user)

session.commit