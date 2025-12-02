from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from src.app.db.database import get_db
from src.app.db.models.user import User
from src.app.api.schemas.user import UserCreate, UserLogin, UserRead


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Password hashing instance
pswd_hash = PasswordHash.recommended()


# -----------------------------------------------------------------------------
# SIGNUP
# -----------------------------------------------------------------------------
@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):

    # Check if username or email already exists
    existing = (
        db.query(User)
        .filter((User.username == payload.username) | (User.email == payload.email))
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already taken"
        )

    # Hash the password using pwdlib
    hashed_password = pswd_hash.hash(payload.password)

    # Create the user
    new_user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserRead(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        created_at=str(new_user.created_at),
    )


# -----------------------------------------------------------------------------
# LOGIN
# -----------------------------------------------------------------------------
@router.post("/login", response_model=UserRead)
def login(payload: UserLogin, db: Session = Depends(get_db)):

    # Find the user by username OR email
    user = (
        db.query(User)
        .filter(
            (User.username == payload.username) |
            (User.email == payload.username)
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify password using pwdlib
    if not pswd_hash.verify(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=str(user.created_at),
    )
