from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.db.database import get_db
from src.app.db.models.user import User
from src.app.api.schemas.user import UserCreate, UserRead ##gotta make
from src.app.utils.security import hash_password

# This has all of the user routes



#Signup...username, email, password

router = APIRouter(prefix="/auth", tags=["Auth"])

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
    hashed_pw = hash_password(payload.password)

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


#Login (authenticate user with email and password)


#Change email, username, password