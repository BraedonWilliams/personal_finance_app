from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash


from src.app.db.database import get_db
from src.app.db.models.user import User
from src.app.api.schemas.user import UserCreate, UserLogin, UserRead, UserUpdate, PassUpdate ##gotta make
#from src.app.utils.security import hash_password
#remember to go into security and delete that since you just did pwdlib instead of making your own


################# SIGNUP ###################
router = APIRouter(prefix="/auth", tags=["Auth"])
pswd_hash = PasswordHash.recommended() #create an instance of PasswordHash (Argon2 is recommended)

@router.post("/signup", response_model=UserRead)
def signup(payload: UserCreate, db: Session = Depends(get_db)):


    # Check if username or email already exists
    existing_user = (
        db.query(User)
        .filter((User.username == payload.username) | (User.email == payload.email))
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

    # Hash the password
    hashed_pw = pswd_hash(payload.password)

    # Create user object
    new_user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hashed_pw,
    )

    # Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return response
    return UserRead(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        created_at=str(new_user.created_at)
    )


########LOGIN############# (authenticate user with email and password)
@router.post("/login", response_model=UserRead)
def login(payload: UserLogin, db: Session = Depends(get_db)):

     # Check if username or email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    # if the email isn't in the database...
    if not existing_user:
        raise HTTPException(404, "User not found")
    
    if not pswd_hash.verify(payload.password, existing_user.password_hash):
        raise HTTPException(401, "Incorrect Password")
    
    # check if the username/email and the password that's entered line up. IF they do, then you return the requested information.
    #return response
    return UserRead(
        id=existing_user.id,
        username=existing_user.username,
        email=existing_user.email,
        created_at=str(existing_user.created_at)
    )

""" #Change email, username, password
@router.patch("/update", response_model=UserRead)
def update(payload: UserUpdate, db: Session = Depends(get_db)):
    current_user =(
        db.query(User)
        .filter(User.email)
        .first()
    )
 """