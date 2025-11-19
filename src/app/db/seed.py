from database import SessionLocal, User

db = SessionLocal()

user = User(username="firstUser", password_hash="password", email="firstUser@gmail.com")

db.add(user)
db.commit()
db.close()
