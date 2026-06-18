from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from database import get_db
from models import User
from schemas import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])


def hash_password(password: str):
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str):
    password_bytes = password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id,
        "username": new_user.username
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "message": "Login successful",
        "user_id": existing_user.id,
        "username": existing_user.username
    }